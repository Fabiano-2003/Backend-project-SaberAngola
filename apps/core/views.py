from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Setting
from .serializers import SettingSerializer, PublicSettingSerializer, SettingCreateSerializer

class SettingViewSet(viewsets.ModelViewSet):
    queryset = Setting.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = SettingSerializer
    
    def get_serializer_class(self):
        if self.action == 'public':
            return PublicSettingSerializer
        return self.serializer_class
    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.AllowAny]
    )
    def public(self, request):
        settings = Setting.objects.filter(is_public=True)
        serializer = self.get_serializer(settings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        if not isinstance(request.data, list):
            return Response(
                {'error': 'Expected a list of settings'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        updated = []
        errors = []
        
        for index, item in enumerate(request.data):
            try:
                # Find existing setting by key
                if not isinstance(item, dict) or 'key' not in item:
                    errors.append({
                        'index': index,
                        'error': 'Item must be a dict with "key" field',
                        'item': item
                    })
                    continue
                
                setting = Setting.objects.filter(key=item['key']).first()
                if not setting:
                    errors.append({
                        'index': index,
                        'error': f'Setting with key "{item["key"]}" not found'
                    })
                    continue
                
                # Use serializer for validation
                serializer = SettingSerializer(setting, data=item, partial=True)
                if serializer.is_valid():
                    updated_setting = serializer.save()
                    updated.append(updated_setting)
                else:
                    errors.append({
                        'index': index,
                        'key': item['key'],
                        'errors': serializer.errors
                    })
                    
            except Exception as e:
                errors.append({
                    'index': index,
                    'error': str(e),
                    'item': item
                })
        
        response_data = {
            'updated': SettingSerializer(updated, many=True).data,
            'updated_count': len(updated),
            'total_processed': len(request.data)
        }
        
        if errors:
            response_data['errors'] = errors
            response_data['error_count'] = len(errors)
            
        # Return partial success if some items were processed
        response_status = status.HTTP_200_OK if updated else status.HTTP_400_BAD_REQUEST
        if errors and updated:
            response_status = status.HTTP_207_MULTI_STATUS
            
        return Response(response_data, status=response_status)
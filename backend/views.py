from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        week = self.request.query_params.get('week')
        year = self.request.query_params.get('year')
        queryset = Event.objects.all()
        
        if week and year:
            queryset = queryset.filter(week_number=week, year=year)
        return queryset

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        event = self.get_object()
        
        try:
            vote = Vote.objects.create(
                user=request.user,
                event=event
            )
            
            # Update status based on vote position
            total_votes = event.votes.count()
            if total_votes <= 6:
                vote.status = 'playing'
            else:
                vote.status = 'standby'
            vote.save()
            
            return Response({'status': 'vote recorded'})
        except ValidationError as e:
            return Response({'error': str(e)}, status=400) 
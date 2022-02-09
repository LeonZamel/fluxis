from django.urls import path, include

from authentication.views import (
    CredentialsList,
    CredentialsDetail,
    DatabaseServiceList,
    DatabaseCredentialsCreate,
    OAuth2ServiceList,
    OAuth2Start,
    OAuth2Callback,
)

from .views import (
    NodeList,
    NodeDetail,
    UserDetail,
    UserList,
    InitView,
    EdgeList,
    EdgeDetail,
    FlowList,
    FlowDetail,
    FlowConfigDetail,
    HttpEndpointDetail,
    ConstantValueList,
    ConstantValueDetail,
    HttpEndpointTriggerList,
    TimerTriggerList,
    TriggerList,
    FlowRunList,
    FlowRunDetail,
    NodeRunDetail,
    FlowRunScheduleList,
    FlowRunScheduleDetail,
    FileList,
)

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    path('init/', InitView.as_view()),

    path('flows/<g_pk>/nodes/', NodeList.as_view()),
    path('flows/<g_pk>/nodes/<pk>/', NodeDetail.as_view()),
    path('flows/<g_pk>/edges/', EdgeList.as_view()),
    path('flows/<g_pk>/edges/<pk>/', EdgeDetail.as_view()),
    path('flows/<g_pk>/runs/<r_pk>/<pk>/', NodeRunDetail.as_view()),

    # Currently not using g_pk
    path('flows/<g_pk>/runs/<pk>/', FlowRunDetail.as_view()),
    path('flows/<g_pk>/runs/', FlowRunList.as_view()),
    path('flows/<g_pk>/schedules/<pk>/', FlowRunScheduleDetail.as_view()),
    path('flows/<g_pk>/schedules/', FlowRunScheduleList.as_view()),
    path('flows/<pk>/config/', FlowConfigDetail.as_view()),
    path('flows/<pk>/', FlowDetail.as_view()),
    path('flows/', FlowList.as_view()),

    path('http_endpoint/<pk>', HttpEndpointDetail.as_view()),

    path('triggers/http_endpoint/', HttpEndpointTriggerList.as_view()),
    path('triggers/timer/', TimerTriggerList.as_view()),
    path('triggers/', TriggerList.as_view()),

    path('runs/', FlowRunList.as_view()),

    path('auth/credentials/', CredentialsList.as_view()),
    path('auth/credentials/<pk>/', CredentialsDetail.as_view()),
    path('auth/oauth2/services/', OAuth2ServiceList.as_view()),
    path('auth/database/', DatabaseCredentialsCreate.as_view()),
    path('auth/database/services/', DatabaseServiceList.as_view()),

    path('oauth2/start/', OAuth2Start.as_view()),
    path('oauth2/callback/', OAuth2Callback.as_view()),

    path('files/', FileList.as_view()),

    # path('users/', UserList.as_view()),
    # path('users/<int:pk>/', UserDetail.as_view()),
]

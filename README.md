# Модуль для работы с Mattermost API
___

### Предоставляет средства для связи с Mattermost через 
* REST API
* websocket

## Требуемая секции в конфиге:
___


    mattermost:
      http_host: "https://{mattermost_host}"
      api_location: "/api/v4/"
      api_version: "4"
      token: "{mm_token}"
      id: "{mm_id}"
      listen_channels:
        - "{channel_for_listen_1}"
        - "{channel_for_listen_2}"
      target_events_processors:
        - posted:
           - "save"
           - "response"
        - hello:
           - "log"
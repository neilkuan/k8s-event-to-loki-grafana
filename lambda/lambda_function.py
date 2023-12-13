import json
def level_helper(event_type, message, reason):
    level = 'info'
    if 'error' in message.lower():
        level = 'error'
        return level
    if 'unhealthy' in reason.lower():
        level = 'error'
        return level
    if event_type == 'Warning':
        level = 'warning'
        return level
    if event_type == 'Normal':
        level = 'info'
        return level
    return level
def lambda_handler(event, context):
    print(event)
    try:
        
        body_json = json.loads(event.get('body'))
        reason = body_json.get('reason')
        message = body_json.get('message')
        event_type = body_json.get('type')
        namespace = body_json.get('metadata').get('namespace')
        kind = body_json.get('involvedObject').get('kind')
        name = body_json.get('involvedObject').get('name')
        data_cluster = event.get('headers').get('data-center')
        # print json format for CloudWacth Logs Insights parse
        # level key for Grafana display color for log
        # dataCenter for filter dataCentor in future
        # details for need more details on Grafana
        print({
            "msg": f"[{namespace}] [{kind}] \"{name}\" [{reason}] {message}",
            "query_all": "all",
            "level": f"{level_helper(event_type ,message , reason)}",
            "dataCenter": f"{data_cluster}",
            "details": f"{body_json}"
        })
    except Exception as e:
        print({
            "msg": f"Parse Exception {e}",
            "query_all": "all",
            "level": "unknown",
            "dataCenter": "none",
            "details": f"{event}"
        })
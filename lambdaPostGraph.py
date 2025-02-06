import json
import boto3

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('cityDistances')

    try:
        while True:
            scan_kwargs = {}
            response = table.scan(**scan_kwargs)
            items = response['Items']

            for item in items:
                key = {
                    'cityToCity': item['cityToCity'],  # Use item['cityToCity'] directly (it's already {'S': 'value'})
                    'distance': item['distance']       # Use item['distance'] directly (it's already {'N': 123})
                }
                table.delete_item(Key=key)

            if 'LastEvaluatedKey' not in response:
                break
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']

    except Exception as e:
        return {
            "statusCode": 400, 
            "body": "Error Delete Previous Items In Graph"
        }

    try:
        # Format Input And Create Graph
        graph_string = event['graph']
        graph_edges = graph_string.split(",")

        graph = {}
        cities = set()

        for edge in graph_edges:
            city1, city2 = edge.split("->")

            graph[city1] = graph.get(city1, []) + [city2]
            
            cities.add(city1)
            cities.add(city2)

        # BFS While inserting into DynamoDb
        for city in cities:
            next_cities = graph.get(city, [])
            cur_dist = 1
            visited_cities = {city}

            while next_cities != []:
                new_next_cities = []

                for ncity in next_cities:
                    if ncity not in visited_cities:
                        visited_cities.add(ncity)

                        table.put_item(
                            Item={
                                "cityToCity": city + ", " + ncity, 
                                "distance": cur_dist
                            }
                        )
                        new_next_cities.extend(graph.get(ncity, []))
                
                cur_dist += 1
                next_cities = new_next_cities

        return {
            "statusCode": 200, 
            "body": "Successfully Saved Graph"
        }
    except:
        return {
            "statusCode": 400, 
            "body": "Error Saving Graph"
        }
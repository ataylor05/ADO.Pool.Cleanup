from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import json
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
app.config["DEBUG"] = True

def getPoolId(taskAgentClient, name):
    pools = taskAgentClient.get_agent_pools()
    for pool in pools:
        if pool.name == name:
            return pool.id

def getAgentList(taskAgentClient, poolId):
    return taskAgentClient.get_agents(pool_id=poolId)

def removeOfflineAgents(taskAgentClient, poolId, agentList):
    for agent in agentList:
        if agent.status == "offline":
            taskAgentClient.delete_agent(pool_id=poolId, agent_id=agent.id)

@app.route("/", methods=["GET"])
def cleanPool():
    poolName = str(request.json.get('poolName', ''))
    pat = str(request.json.get('pat', ''))
    org = str(request.json.get('org', ''))
    #
    credentials = BasicAuthentication('', pat)
    connection = Connection(base_url=org, creds=credentials)
    taskAgentClient = connection.clients.get_task_agent_client()
    #
    poolId = getPoolId(taskAgentClient, poolName)
    agentList = getAgentList(taskAgentClient, poolId)
    removeOfflineAgents(taskAgentClient, poolId, agentList)
    return "success"

app.run(host='0.0.0.0', ssl_context='adhoc')

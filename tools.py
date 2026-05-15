from enum import StrEnum

# In real product we would probably want to add more tools. I chose the network-specific ones, because that's
# the problem I'm solving in my demonstration notebook.

def format_tools() -> str:
    return "\n".join(f"- {tool}" for tool in Tools)

class Tools(StrEnum):
    INSPECT_INTERFACE = (
        "INSPECT_INTERFACE: Diagnostic command used to read current settings, "
        "MTU limits, and encapsulation parameters on a specific target router "
        "interface (e.g., 'show interfaces GigabitEthernet0/1')."
    )
    MONITOR_OSPF_NEIGHBORS = (
        "MONITOR_OSPF_NEIGHBORS: Operational command used to query the routing "
        "protocol state machine, verify neighbor relationships, and detect stuck "
        "states like EXSTART or DOWN (e.g., 'show ip ospf neighbor')."
    )
    MODIFY_ROUTER_CONFIGURATION = (
        "MODIFY_ROUTER_CONFIGURATION: Execution command used to push terminal "
        "configuration blocks (e.g., entering configuration mode, altering MTU "
        "parameters, or modifying interface flags) to a specific hardware node."
    )
    FETCH_SERVICE_LOGS = (
        "FETCH_SERVICE_LOGS: System primitive used to extract execution streams "
        "and exception states from application layers, including gRPC connection "
        "timeouts and RabbitMQ queue metrics."
    )

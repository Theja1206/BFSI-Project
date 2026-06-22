import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from agent_graph import credit_agent_app



def run_risk_evaluation(customer_id:str):
    print(f"\n --- Initalizing agentic risk review for {customer_id}---")

    initial_input = {
        "messages":[
            HumanMessage(content=f"Please audit the credit risk profile for customer{customer_id}"
                                  f"Check their Internal bank finance ratio and look for external credit beureau flags"
                                  f"Provided summary final approval decision")
        ]
    }

    for event in credit_agent_app.stream(initial_input):
        for node, data in event.items():
            print(f"\n [Node Activated: {node}]")
            latest_msg = data["messages"][-1]
            if hasattr(latest_msg, 'tool_calls') and latest_msg.tool_calls:
                print(f"Agent requested tool invocation : {latest_msg.tool_calls[0]['name']}")
            
            else:
                print(f"Content:{latest_msg.content}")



if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Please export your Anthropic API Key to continue")
    else:
        run_risk_evaluation("CUST101")
        run_risk_evaluation("CUST102")

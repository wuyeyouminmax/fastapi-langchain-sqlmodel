from langgraph.constants import START, END
from langgraph.graph import StateGraph

from wuyou.agent.node.MessageNode import MessageNode
from wuyou.agent.node.MessageState import MessageState

# 图rgaph
class MessageGraph:
    def __init__(self):
        self.graph = None

    async def build_demo_graph(self, message_node: MessageNode):
        graph_build = StateGraph(MessageState)
        graph_build.add_node("demo_crate_score", message_node.demo_crate_score)
        graph_build.add_node("demo_winner", message_node.demo_winner)
        graph_build.add_node("demo_loser", message_node.demo_loser)

        graph_build.add_edge(START, "demo_crate_score")
        graph_build.add_conditional_edges(
            "demo_crate_score",
            message_node.demo_check,
            {"winner": "demo_winner", "loser": "demo_loser"}
        )
        graph_build.add_edge("demo_winner", END)
        graph_build.add_edge("demo_loser", END)

        self.graph = graph_build.compile()
        return self.graph

    async def run_runnable(self, data: int, message_node: MessageNode):
        runnable = await self.build_demo_graph(message_node)
        result = await runnable.ainvoke({"user_data": data})
        return result

from langgraph.constants import START, END
from langgraph.graph import StateGraph

from wuyou.agent.node.MessageNode import MessageNode, get_message_node
from wuyou.agent.node.MessageState import MessageState

# 图rgaph
class MessageGraph:
    def __init__(self, message_node: MessageNode):
        self.message_node = message_node

    @classmethod
    async def create(cls):
        data_base_node = await get_message_node()
        return cls(data_base_node)

    async def build_demo_graph(self):
        """构建一个工作流graph(图)"""
        # 在这个图中流转的信息state
        print("开始构建图")
        graph_build = StateGraph(MessageState)
        #添加各点
        print("开始构建各个节点")
        graph_build.add_node("demo_crate_score",self.message_node.demo_crate_score)
        graph_build.add_node("demo_winner",self.message_node.demo_winner)
        graph_build.add_node("demo_loser",self.message_node.demo_loser)
        print("节点添加完毕")
        # 链接边
        print("开始构建边")
        graph_build.add_edge(START,"demo_crate_score")
        # 链接判断点
        graph_build.add_conditional_edges(
            "demo_crate_score",
            self.message_node.demo_check,
            {
                "winner":"demo_winner",
                "loser":"demo_loser"
            }
        )
        graph_build.add_edge("demo_winner",END)
        graph_build.add_edge("demo_loser", END)
        print("边构建完毕")
        return graph_build.compile()

    async def run_runnable(self,data:int):
        """"""
        runnable = await self.build_demo_graph()
        print("开始运行图")
        result = await runnable.ainvoke({"user_data": data})
        print("运行完毕")
        return result

async def get_message_graph()->MessageGraph:
    if not hasattr(get_message_graph,"instance"):
        get_message_graph.instance = await MessageGraph.create()
    return get_message_graph.instance
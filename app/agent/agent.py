from langgraph.graph import StateGraph
from pydantic import BaseModel
from knowledge_base.vectore_store import ChromaVectorTool
from agent.tools.web_search import DuckDuckGoWebReaderTool
from langchain.llms import HuggingFacePipeline
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM


class AgentState(BaseModel):
    input: str
    context: str = ""
    response: str = ""

class Agent:
    def __init__(self):
        # self.chroma_tool = ChromaVectorTool()
        self.web_tool = DuckDuckGoWebReaderTool()

        tokenizer = AutoTokenizer.from_pretrained("Doctor-Shotgun/TinyLlama-1.1B-32k-Instruct", token='')
        model = AutoModelForCausalLM.from_pretrained("Doctor-Shotgun/TinyLlama-1.1B-32k-Instruct", token='')
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
        self.llm = HuggingFacePipeline(pipeline=pipe)

        self.graph = self._build_graph()

    def _build_graph(self):
        def router(state: AgentState) -> str:
            query = state.input.lower()
            next_node = "web_tool" if "интернет" in query or "найди" in query else "chroma_tool"

            return {"next": next_node}

        def web_node(state: AgentState):
            return {"context": self.web_tool.run(state.input)}

        def chroma_node(state: AgentState):
            return {"context": self.chroma_tool.run(state.input)}

        def answer_node(state: AgentState):
            prompt = f"Контекст:\n{state.context}\n\nВопрос: {state.input}\nОтвет:"
            result = self.llm(prompt)[0]["generated_text"]

            return {"response": result[len(prompt):].strip()}

        graph = StateGraph(AgentState)
        graph.add_node("router", router)
        graph.add_node("web_tool", web_node)
        graph.add_node("chroma_tool", chroma_node)
        graph.add_node("answer", answer_node)

        graph.set_entry_point("router")
        graph.add_conditional_edges("router", router)
        graph.add_edge("web_tool", "answer")
        graph.add_edge("chroma_tool", "answer")
        graph.set_finish_point("answer")

        return graph.compile()

    def run(self, question: str) -> str:
        result = self.graph.invoke({"input": question})

        return result

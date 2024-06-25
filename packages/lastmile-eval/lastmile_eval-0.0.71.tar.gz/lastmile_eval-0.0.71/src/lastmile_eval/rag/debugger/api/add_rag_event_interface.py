"""Interface for defining the methods for adding rag-specific events"""

import abc
import json
from dataclasses import asdict
from typing import Any, Optional, TYPE_CHECKING, Union

from opentelemetry.trace.span import Span

from ..common.types import Node, RetrievedNode, TextEmbedding, RagFlowType

if TYPE_CHECKING:
    from _typeshed import DataclassInstance

# Define custom event types
CHUNKING = "chunking"
EMBEDDING = "embedding"
MULTI_EMBEDDING = "multi_embedding"
PROMPT_COMPOSITION = "prompt_composition"
QUERY = "query"
RETRIEVAL = "retrieval"
SYNTHESIZE = "synthesize"
SUB_QUESTION = "sub_question"
TEMPLATING = "templating"
TOOL_CALL = "tool_call"
RERANKING = "reranking"


# TODO: Add exception handling events
class AddRagEventInterface(abc.ABC):
    """
    Interface for defining the rag-specific events. Each rag-specific event calls
    into add_rag_event_for_span() to add the event for a span.

    The method `add_rag_event_for_span` needs to be implemented by whichever
    class implements this interface (Python does not have interfaces so this
    is done through a child class inheriting AddRagEventInterface).
    """

    def add_query_event(
        self,
        query: str,
        llm_output: str | list[str],
        system_prompt: Optional[str] = None,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Use this to keep track of the start and end of a query.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        if system_prompt is not None:
            if metadata is None:
                metadata = {}
            metadata["system_prompt"] = system_prompt
        self.add_rag_event_for_span(
            event_name=event_name or QUERY,
            span=span,
            input=query,
            output=llm_output,  # TODO(rossdan): Make it str only to make everything else easier
            should_also_save_in_span=should_also_save_in_span,
            event_data=metadata,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=QUERY,
        )

    def add_chunking_event(
        self,
        output_nodes: list[Node],
        filepath: Optional[str] = None,
        retrieved_node: Optional[RetrievedNode] = None,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Use this to keep track of nodes generated either from:
            1. a file (ingestion)
            2. RetrievedNode (retrieval)
                if you desire to sub-chunk your retrieved nodes

        @param filepath: The path to the file that was chunked
            If this is not provided, retrieved_node must be provided
        @param retrieved_node: The retrieved node that was chunked
            If this is not provided, filepath must be provided
        @param output_nodes: The nodes generated from the chunking process

        You can use metadata to store other information such chunk size,
        mime type, file metadata, etc.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        if filepath is None and retrieved_node is None:
            print(
                "Warning: You must either provide a filepath or a retrieved node in order to chunk text"
            )
            return
        if filepath is not None and retrieved_node is not None:
            print(
                "Warning: You must provide either a filepath or a retrieved node, not both"
            )
            return
        input_text: str = ""
        if filepath:
            input_text = filepath
        if retrieved_node:
            input_text = retrieved_node.text

        output_nodes_serialized = json.dumps(list(map(asdict, output_nodes)))

        self.add_rag_event_for_span(
            event_name=event_name or CHUNKING,
            span=span,
            input=input_text,
            output=output_nodes_serialized,
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=CHUNKING,
        )

    def add_embedding_event(
        self,
        embedding: TextEmbedding,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Use this to keep track of the embeddings generated from text in either:
            1. the query during retrieval
            2. the documents during ingestion

        You can use metadata to store other information such as the embedding
        model name.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        self.add_rag_event_for_span(
            event_name=event_name or EMBEDDING,
            span=span,
            input=embedding.text,
            output=embedding.vector,
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=EMBEDDING,
        )

    def add_multi_embedding_event(
        self,
        embeddings: list[TextEmbedding],
        rounding_decimal_places: int = 4,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Similar to add_embedding_event() but for multiple TextEmbedding objects.

        @param rounding_decimal_places: The number of decimal places to round
            each float value in the embedding vectors to. We need to do this
            because OpenTelemetry doesn't support nested lists in span
            attributes, so we need to convert the nested list of embeddings
            to a json string. However, for floats with long decimal places,
            this can cause the string to be too large for OpenTelemetry to
            handle (floats are 64-bit, strings are 8-bit per char) and fail
            with a "413 Request Entity Too Large" error.

            If this happens, you can also try reducing the size of your
            payload calls by splitting up `add_multi_embedding_event`
            within separate sub-spans and using `add_embedding_event()`
            instead.

            Example:
            ```
            # Before
            tracer.add_multi_embedding_event(
                embeddings=embeddings,
                span=span,
            )

            # After
            for embedding in embeddings:
                with tracer.start_as_current_span(
                    "sub-embedding",
                    context=span.get_span_context() #Connect to parent span
                ) as sub_span:
                    tracer.add_embedding_event(
                        embedding=embedding,
                        span=sub_span,
                    )
            tracer.add_synthesize_event(
                input="Synthesized embedings",
                output="Success!",
                span=span,
            )
            ```

        You can use metadata to store other information such as the embedding
        model name, text count, etc.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        clipped_vectors: list[list[float]] = [
            [round(j, rounding_decimal_places) for j in i.vector]
            for i in embeddings
        ]

        self.add_rag_event_for_span(
            event_name=event_name or MULTI_EMBEDDING,
            span=span,
            input=[embedding.text for embedding in embeddings],
            # Span attributes can only be primitives or lists of primitives
            # clipped_vectors are in list[list[float]] format so we need to
            # dump to str
            output=json.dumps(clipped_vectors),
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=MULTI_EMBEDDING,
        )

    def add_prompt_composition_event(
        self,
        resolved_prompt: str,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
    ):
        """
        Use this to keep track of how a prompt is composed from multiple
        sources such as the system prompt, user prompt, and retrieved context.
        This event represents the synthesis of all these sources (from child span events)
        into a single resolved prompt.


        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        self.add_rag_event_for_span(
            event_name=event_name or PROMPT_COMPOSITION,
            span=span,
            input="",
            output=resolved_prompt,
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            span_kind=PROMPT_COMPOSITION,
        )

    def add_sub_question_event(
        self,
        original_query: str,
        subqueries: list[str],
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Use this to keep track of whenever a query is split into smaller
        sub-questions to be handled separately later.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        self.add_rag_event_for_span(
            event_name=event_name or SUB_QUESTION,
            span=span,
            input=original_query,
            output=subqueries,
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=SUB_QUESTION,
        )

    def add_retrieval_event(
        self,
        query: str,
        retrieved_nodes: list[RetrievedNode],  # Can also make this str
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Use this to keep track of the nodes retrieved for a query.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        retrieved_nodes_serialized = json.dumps(
            list(map(asdict, retrieved_nodes))
        )
        self.add_rag_event_for_span(
            event_name=event_name or RETRIEVAL,
            span=span,
            input=query,
            output=retrieved_nodes_serialized,
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=RETRIEVAL,
        )

    def add_reranking_event(
        self,
        input_nodes: list[Node],
        output_nodes: list[Node],
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Use this to keep track on how nodes that were retrieved are re-ordered

        You can use metadata to store other information such as the re-ranking
        model name.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        input_nodes_as_dict = list(map(lambda node: asdict(node), input_nodes))
        output_nodes_as_dict = list(
            map(lambda node: asdict(node), output_nodes)
        )
        self.add_rag_event_for_span(
            event_name=event_name or RERANKING,
            span=span,
            # TODO: Fix dict issue with span events
            input=input_nodes_as_dict,
            output=output_nodes_as_dict,
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=RERANKING,
        )

    def add_template_event(
        self,
        prompt_template: str,
        resolved_prompt: str,
        system_prompt: Optional[str] = None,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Use this to keep track on how a query is re-written using a prompt
        template

        You can use metadata to store other information such as the original
        user question, retrieved context, prompt template id, etc.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        if system_prompt is not None:
            if metadata is None:
                metadata = {}
            metadata["system_prompt"] = system_prompt
        self.add_rag_event_for_span(
            event_name=event_name or TEMPLATING,
            span=span,
            input=prompt_template,
            output=resolved_prompt,
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=TEMPLATING,
        )

    def add_tool_call_event(
        self,
        tool_name: str,
        # TODO: Result and value of tool_arguments can't actually be Any,
        # it must be JSON-serializable
        tool_arguments: dict[str, Any],
        tool_result: Any,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Use this to keep track on how a query invokes a tool call

        You can use metadata to store other information such as the tool
        parameter schema, tool parameter values, pre-processed result, etc.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        self.add_rag_event_for_span(
            event_name=event_name or TOOL_CALL,
            span=span,
            # TODO: Fix dict issue
            input={"tool_name": tool_name, "tool_arguments": tool_arguments},
            output=tool_result,
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=TOOL_CALL,
        )

    def add_synthesize_event(
        self,
        input: Any,
        output: Any,
        span: Optional[Span] = None,
        event_name: Optional[str] = None,
        should_also_save_in_span: bool = True,
        metadata: Optional[dict[str, Any]] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ):
        """
        Use this as a catch-all to summarize the input and output of several
        nested events.

        This calls into the `add_rag_event_for_span` method so please see the
        docstrings there on how to use any of the shared arguments.
        """
        self.add_rag_event_for_span(
            event_name=event_name or SYNTHESIZE,
            span=span,
            # TODO: Fix dict issue for span data
            input=input,
            output=output,
            event_data=metadata,
            should_also_save_in_span=should_also_save_in_span,
            ingestion_trace_id=ingestion_trace_id,
            rag_flow_type=rag_flow_type,
            span_kind=SYNTHESIZE,
        )

    @abc.abstractmethod
    def add_rag_event_for_span(
        self,
        event_name: str,
        span: Optional[Span] = None,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[
            Union[dict[Any, Any], "DataclassInstance"]
        ] = None,
        should_also_save_in_span: bool = True,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
        # TODO: Make span_kind an enum so easier to use
        span_kind: Optional[str] = None,
    ) -> None:
        """
        Add a RagEvent for a specific span within a trace. This event gets
        saved at the end of the trace to the RagEvents table, where you can use
        these events to generate test cases and run evaluation metrics on them.
        To run evaluations, you can either use the (`input`, `output`) data
        fields explicitly, or you can use the unstructured `event_data` JSON.

        If all three of those fields aren't included (`input`, `output`,
        `event_data`), an error will be thrown.

        You can only call this method once per span, otherwise it will raise
        an error.

        @param event_name (str): The name of the event
        @param span Optional(Span): The span to add the event to. If None, then
            we use the current span
        @param input Optional(dict[Any, Any]): The input data for the event
        @param output Optional(dict[Any, Any]): The output data for the event
        @param event_data Optional(dict[Any, Any]): The unstructured event data
            in JSON format or Dataclass where you can customize what fields
            you want to use later in your evaluation metrics
        @param should_also_save_in_span (bool): Whether to also save this data
            in the current span events. Defaults to true
        @param ingestion_trace_id Optional(str): The id of a trace used during
            indexing or ingesting your data pipeline to help link the query
            flow to the state of your RAG data state
        @param rag_flow_type Optional[RagFlowType]: The type of RAG flow that
            this trace is being used for. If it is none, then we check for the
            `rag_flow_type` argument that was passed in the
            `get_lastmile_tracer()` call to generate the tracer object that
            calls this method.
        @param span_kind Optional(str): The type of span this is.
        """

    @abc.abstractmethod
    def add_rag_event_for_trace(
        self,
        event_name: str,
        # TODO: Have better typing for JSON for input, output, event_data
        input: Any = None,
        output: Any = None,
        event_data: Optional[
            Union[dict[Any, Any], "DataclassInstance"]
        ] = None,
        ingestion_trace_id: Optional[str] = None,
        rag_flow_type: Optional[RagFlowType] = None,
    ) -> None:
        """
        This is the same functionality as `add_rag_event_for_span()` except
        this is for recording events at the overall trace level. This is useful
        in case you want to run evaluations on the entire trace, rather than
        individual span events.

        You can only call this method once per trace, otherwise it will raise
        an error.
        """

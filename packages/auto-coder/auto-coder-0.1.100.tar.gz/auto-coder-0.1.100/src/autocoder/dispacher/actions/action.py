from autocoder.common import (
    AutoCoderArgs,
    TranslateArgs,
    TranslateReadme,
    split_code_into_segments,
    SourceCode,
)
from autocoder.pyproject import PyProject, Level1PyProject
from autocoder.tsproject import TSProject
from autocoder.suffixproject import SuffixProject
from autocoder.index.index import build_index_and_filter_files
from autocoder.common.code_auto_merge import CodeAutoMerge
from autocoder.common.code_auto_merge_diff import CodeAutoMergeDiff
from autocoder.common.code_auto_merge_strict_diff import CodeAutoMergeStrictDiff
from autocoder.common.code_auto_merge_editblock import CodeAutoMergeEditBlock
from autocoder.common.code_auto_generate import CodeAutoGenerate
from autocoder.common.code_auto_generate_diff import CodeAutoGenerateDiff
from autocoder.common.code_auto_generate_strict_diff import CodeAutoGenerateStrictDiff
from autocoder.common.code_auto_generate_editblock import CodeAutoGenerateEditBlock
from typing import Optional, Generator
import byzerllm
import os
from autocoder.common.image_to_page import ImageToPage, ImageToPageDirectly
from autocoder.utils.conversation_store import store_code_model_conversation
from loguru import logger


class ActionTSProject:
    def __init__(
        self, args: AutoCoderArgs, llm: Optional[byzerllm.ByzerLLM] = None
    ) -> None:
        self.args = args
        self.llm = llm
        self.pp = None

    def run(self):
        args = self.args
        if args.project_type != "ts":
            return False
        pp = TSProject(args=args, llm=self.llm)
        self.pp = pp
        pp.run()

        source_code = pp.output()
        if self.llm:
            source_code = build_index_and_filter_files(
                llm=self.llm, args=args, sources=pp.sources
            )

        if args.image_file:
            if args.image_mode == "iterative":
                image_to_page = ImageToPage(llm=self.llm, args=args)
            else:
                image_to_page = ImageToPageDirectly(llm=self.llm, args=args)

            file_name = os.path.splitext(os.path.basename(args.image_file))[0]
            html_path = os.path.join(
                os.path.dirname(args.image_file), "html", f"{file_name}.html"
            )
            image_to_page.run_then_iterate(
                origin_image=args.image_file,
                html_path=html_path,
                max_iter=self.args.image_max_iter,
            )

            with open(html_path, "r") as f:
                html_code = f.read()
                source_code = f"##File: {html_path}\n{html_code}\n\n" + source_code

        self.process_content(source_code)
        return True

    def process_content(self, content: str):
        args = self.args

        if args.execute and self.llm and not args.human_as_model:
            if len(content) > self.args.model_max_input_length:
                logger.warning(
                    f"Content length is {len(content)}, which is larger than the maximum input length {self.args.model_max_input_length}. chunk it..."
                )
                content = content[: self.args.model_max_input_length]

        if args.execute:
            logger.info("Auto generate the code...")
            if args.auto_merge == "diff":
                generate = CodeAutoGenerateDiff(
                    llm=self.llm, args=self.args, action=self
                )
            elif args.auto_merge == "strict_diff":
                generate = CodeAutoGenerateStrictDiff(
                    llm=self.llm, args=self.args, action=self
                )
            elif args.auto_merge == "editblock":
                generate = CodeAutoGenerateEditBlock(
                    llm=self.llm, args=self.args, action=self
                )
            else:
                generate = CodeAutoGenerate(llm=self.llm, args=self.args, action=self)
            if self.args.enable_multi_round_generate:
                result, conversations = generate.multi_round_run(
                    query=args.query, source_content=content
                )
            else:
                result, conversations = generate.single_round_run(
                    query=args.query, source_content=content
                )
            content = "\n\n".join(result)

            store_code_model_conversation(
                args=self.args,
                instruction=self.args.query,
                conversations=conversations,
                model=self.llm.default_model_name,
            )
        with open(args.target_file, "w") as file:
            file.write(content)

        if args.execute and args.auto_merge:
            logger.info("Auto merge the code...")
            if args.auto_merge == "diff":
                code_merge = CodeAutoMergeDiff(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            elif args.auto_merge == "strict_diff":
                code_merge = CodeAutoMergeStrictDiff(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            elif args.auto_merge == "editblock":
                code_merge = CodeAutoMergeEditBlock(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            else:
                code_merge = CodeAutoMerge(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)


class ActionPyScriptProject:
    def __init__(
        self, args: AutoCoderArgs, llm: Optional[byzerllm.ByzerLLM] = None
    ) -> None:
        self.args = args
        self.llm = llm

    def run(self) -> bool:
        args = self.args
        if args.project_type != "py-script":
            return False
        pp = Level1PyProject(
            script_path=args.script_path, package_name=args.package_name
        )
        content = pp.run()
        self.process_content(content)
        return True

    def process_content(self, content: str):
        args = self.args
        if args.execute:
            if args.auto_merge == "diff":
                generate = CodeAutoGenerateDiff(
                    llm=self.llm, args=self.args, action=self
                )
            elif args.auto_merge == "strict_diff":
                generate = CodeAutoGenerateStrictDiff(
                    llm=self.llm, args=self.args, action=self
                )
            elif args.auto_merge == "editblock":
                generate = CodeAutoGenerateEditBlock(
                    llm=self.llm, args=self.args, action=self
                )
            else:
                generate = CodeAutoGenerate(llm=self.llm, args=self.args, action=self)
            if self.args.enable_multi_round_generate:
                result, conversations = generate.multi_round_run(
                    query=args.query, source_content=content
                )
            else:
                result, conversations = generate.single_round_run(
                    query=args.query, source_content=content
                )
            content = "\n\n".join(result)

            store_code_model_conversation(
                args=self.args,
                instruction=self.args.query,
                conversations=conversations,
                model=self.llm.default_model_name,
            )
        with open(self.args.target_file, "w") as file:
            file.write(content)

        if args.execute and args.auto_merge:
            logger.info("Auto merge the code...")
            if args.auto_merge == "diff":
                code_merge = CodeAutoMergeDiff(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            elif args.auto_merge == "strict_diff":
                code_merge = CodeAutoMergeStrictDiff(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            elif args.auto_merge == "editblock":
                code_merge = CodeAutoMergeEditBlock(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            else:
                code_merge = CodeAutoMerge(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)


class ActionPyProject:
    def __init__(
        self, args: AutoCoderArgs, llm: Optional[byzerllm.ByzerLLM] = None
    ) -> None:
        self.args = args
        self.llm = llm
        self.pp = None

    def run(self):
        args = self.args
        if args.project_type != "py":
            return False
        pp = PyProject(args=self.args, llm=self.llm)
        self.pp = pp
        pp.run(packages=args.py_packages.split(",") if args.py_packages else [])

        source_code = pp.output()
        if self.llm:
            source_code = build_index_and_filter_files(
                llm=self.llm, args=args, sources=pp.sources
            )

        self.process_content(source_code)
        return True

    def process_content(self, content: str):
        args = self.args

        if args.execute and self.llm and not args.human_as_model:
            if len(content) > self.args.model_max_input_length:
                logger.warning(
                    f"Content length is {len(content)}, which is larger than the maximum input length {self.args.model_max_input_length}. chunk it..."
                )
                content = content[: self.args.model_max_input_length]

        if args.execute:
            logger.info("Auto generate the code...")

            if args.auto_merge == "diff":
                generate = CodeAutoGenerateDiff(
                    llm=self.llm, args=self.args, action=self
                )
            elif args.auto_merge == "strict_diff":
                generate = CodeAutoGenerateStrictDiff(
                    llm=self.llm, args=self.args, action=self
                )
            elif args.auto_merge == "editblock":
                generate = CodeAutoGenerateEditBlock(
                    llm=self.llm, args=self.args, action=self
                )
            else:
                generate = CodeAutoGenerate(llm=self.llm, args=self.args, action=self)

            if self.args.enable_multi_round_generate:
                result, conversations = generate.multi_round_run(
                    query=args.query, source_content=content
                )
            else:
                result, conversations = generate.single_round_run(
                    query=args.query, source_content=content
                )
            content = "\n\n".join(result)

            store_code_model_conversation(
                args=self.args,
                instruction=self.args.query,
                conversations=conversations,
                model=self.llm.default_model_name,
            )
        with open(args.target_file, "w") as file:
            file.write(content)

        if args.execute and args.auto_merge:
            logger.info("Auto merge the code...")
            if args.auto_merge == "diff":
                code_merge = CodeAutoMergeDiff(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            elif args.auto_merge == "strict_diff":
                code_merge = CodeAutoMergeStrictDiff(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            elif args.auto_merge == "editblock":
                code_merge = CodeAutoMergeEditBlock(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            else:
                code_merge = CodeAutoMerge(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)


class ActionSuffixProject:
    def __init__(
        self, args: AutoCoderArgs, llm: Optional[byzerllm.ByzerLLM] = None
    ) -> None:
        self.args = args
        self.llm = llm
        self.pp = None

    def run(self):
        args = self.args
        pp = SuffixProject(args=args, llm=self.llm)
        self.pp = pp
        pp.run()
        source_code = pp.output()
        if self.llm:
            source_code = build_index_and_filter_files(
                llm=self.llm, args=args, sources=pp.sources
            )
        self.process_content(source_code)

    def process_content(self, content: str):
        args = self.args

        if args.execute and self.llm and not args.human_as_model:
            if len(content) > self.args.model_max_input_length:
                logger.warning(
                    f"Content length is {len(content)}, which is larger than the maximum input length {self.args.model_max_input_length}. chunk it..."
                )
                content = content[: self.args.model_max_input_length]

        if args.execute:
            logger.info("Auto generate the code...")
            if args.auto_merge == "diff":
                generate = CodeAutoGenerateDiff(
                    llm=self.llm, args=self.args, action=self
                )
            elif args.auto_merge == "strict_diff":
                generate = CodeAutoGenerateStrictDiff(
                    llm=self.llm, args=self.args, action=self
                )
            elif args.auto_merge == "editblock":
                generate = CodeAutoGenerateEditBlock(
                    llm=self.llm, args=self.args, action=self
                )
            else:
                generate = CodeAutoGenerate(llm=self.llm, args=self.args, action=self)
            if self.args.enable_multi_round_generate:
                result, conversations = generate.multi_round_run(
                    query=args.query, source_content=content
                )
            else:
                result, conversations = generate.single_round_run(
                    query=args.query, source_content=content
                )
            content = "\n\n".join(result)

            store_code_model_conversation(
                args=self.args,
                instruction=self.args.query,
                conversations=conversations,
                model=self.llm.default_model_name,
            )

        with open(args.target_file, "w") as file:
            file.write(content)

        if args.execute and args.auto_merge:
            logger.info("Auto merge the code...")
            if args.auto_merge == "diff":
                code_merge = CodeAutoMergeDiff(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            elif args.auto_merge == "strict_diff":
                code_merge = CodeAutoMergeStrictDiff(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            elif args.auto_merge == "editblock":
                code_merge = CodeAutoMergeEditBlock(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)
            else:
                code_merge = CodeAutoMerge(llm=self.llm, args=self.args)
                code_merge.merge_code(content=content)

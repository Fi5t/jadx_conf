#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from io import StringIO
from typing import List


def main(args: List[str]) -> None:
    if not args:
        print("Usage: jadx_conf.py <json config> [additional flags]\nExamples:\n\tjadx_conf.py jadx-example-gui-config.json -e -d app-sources")
        return

    json_config: dict = json.loads(Path(args[0]).read_text())
    cli_config = StringIO()

    if json_config.get('skipResources'):
        cli_config.write('--no-res\n')

    if json_config.get('skipSources'):
        cli_config.write('--no-src\n')

    if json_config.get('exportAsGradleProject'):
        cli_config.write('--export-gradle\n')

    if json_config.get('showInconsistentCode'):
        cli_config.write('--show-bad-code\n')

    if not json_config.get('useImports'):
        cli_config.write('--no-imports\n')

    if not json_config.get('debugInfo'):
        cli_config.write('--no-debug-info\n')

    if json_config.get('addDebugLines'):
        cli_config.write('--add-debug-lines\n')

    if not json_config.get('inlineAnonymousClasses'):
        cli_config.write('--no-inline-anonymous\n')

    if not json_config.get('inlineMethods'):
        cli_config.write('--no-inline-methods\n')

    if not json_config.get('extractFinally'):
        cli_config.write('--no-finally\n')

    if not json_config.get('replaceConsts'):
        cli_config.write('--no-replace-consts\n')

    if json_config.get('escapeUnicode'):
        cli_config.write('--escape-unicode\n')

    if json_config.get('respectBytecodeAccessModifiers'):
        cli_config.write('--respect-bytecode-access-modifiers\n')

    if json_config.get('deobfuscationOn'):
        cli_config.write('--deobf\n')

    if json_config.get('deobfuscationUseSourceNameAsAlias'):
        cli_config.write('--deobf-use-sourcename\n')

    if json_config.get('deobfuscationParseKotlinMetadata'):
        cli_config.write('--deobf-parse-kotlin-metadata\n')

    if json_config.get('fsCaseSensitive'):
        cli_config.write('--fs-case-sensitive\n')

    if json_config.get('cfgOutput'):
        cli_config.write('--cfg\n')

    if json_config.get('rawCfgOutput'):
        cli_config.write('--raw-cfg\n')

    # /!\ Deprecated flag /!\
    if json_config.get('fallbackMode'):
        cli_config.write('--fallback\n')

    if json_config.get('useDx'):
        cli_config.write('--use-dx\n')

    if 'java-convert.d8-desugar' in json_config.get('pluginOptions', []):
        cli_config.write(f'-P\njava-convert.d8-desugar={json_config["pluginOptions"]["java-convert.d8-desugar"]}\n')

    if 'java-convert.mode' in json_config.get('pluginOptions', []):
        cli_config.write(f'-P\njava-convert.mode={json_config["pluginOptions"]["java-convert.mode"]}\n')

    if 'dex-input.verify-checksum' in json_config.get('pluginOptions', []):
        cli_config.write(f'-P\ndex-input.verify-checksum={json_config["pluginOptions"]["dex-input.verify-checksum"]}\n')

    if len(json_config.get('renameFlags', [])) > 0:
        cli_config.write(f'--rename-flags\n{", ".join(json_config["renameFlags"]).lower()}\n')

    cli_config.write(f'--threads-count\n{json_config.get("threadsCount", 4)}\n')
    cli_config.write(f'--decompilation-mode\n{json_config.get("decompilationMode", "AUTO").lower()}\n')
    cli_config.write(f'--deobf-min\n{json_config.get("deobfuscationMinLength", 3)}\n')
    cli_config.write(f'--deobf-max\n{json_config.get("deobfuscationMaxLength", 64)}\n')
    cli_config.write(f'--deobf-cfg-file-mode\n{json_config.get("deobfuscationMapFileMode", "READ").lower()}\n')
    cli_config.write(f'--deobf-res-name-source\n{json_config.get("resourceNameSource", "AUTO").lower()}\n')
    cli_config.write(f'--use-kotlin-methods-for-var-names\n{json_config.get("useKotlinMethodsForVarNames", "APPLY").lower()}\n')
    cli_config.write(f'--comments-level\n{json_config.get("commentsLevel", "INFO").lower()}\n')

    if len(args[1:]) > 0:
        cli_config.write('\n'.join(args[1:]))

    with open('config.jadx', 'w') as f:
        print(cli_config.getvalue(), file=f)

    print(f'{args[0]} converted to config.jadx\nUsage: jadx @config.jadx [options] <input files>')


if __name__ == "__main__":
    main(sys.argv[1:])

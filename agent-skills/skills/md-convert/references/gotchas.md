# md-convert Gotchas

실제 실행 중 자주 부딪히는 환경 이슈와 대응법. `convert.py`가 exit code 3 또는 5로 실패하거나 `pip install`이 실패하면 이 문서를 읽고 해당 항목을 적용한다.

## 1. macOS Homebrew Python — PEP 668로 `pip install` 차단

**증상**
- `pip install 'markitdown[all]'` 실행 시 아래와 유사한 메시지:
  ```
  error: externally-managed-environment
  × This environment is externally managed
  ```

**원인**
- Homebrew로 설치된 Python(`/opt/homebrew/bin/python3`)은 PEP 668 정책에 따라 시스템 위치로의 직접 `pip install`을 막는다.

**대응 (우선순위 순)**
1. **pipx로 CLI 설치** (가장 권장):
   ```bash
   brew install pipx
   pipx install 'markitdown[all]'
   ```
   이후 `markitdown` 명령이 PATH에 등록됨. `convert.py`는 Python API를 쓰므로 pipx만으로는 부족 — 아래 2 또는 3도 같이.
2. **venv로 격리 설치:**
   ```bash
   python3.13 -m venv ~/.venvs/md-convert
   ~/.venvs/md-convert/bin/pip install 'markitdown[all]'
   ```
   이 경우 `convert.py`는 `~/.venvs/md-convert/bin/python`으로 실행해야 한다.
3. **user site-packages 설치:**
   ```bash
   pip install --user --break-system-packages 'markitdown[all]'
   ```
   시스템 Python을 건드리므로 최후 수단.

## 2. Python 3.14에서 `markitdown[all]` 의존성 불만족

**증상**
- `pip install` 중 아래와 유사한 에러:
  ```
  ERROR: Could not find a version that satisfies the requirement
  youtube-transcript-api~=1.0.0; extra == "all"
  ```
- 또는 `markitdown 0.0.2`(아주 오래된 버전)만 설치되는 경우.

**원인**
- `markitdown` 1.x 의존성 트리가 `python<3.14`를 요구. Python 3.14 환경에서는 resolver가 최신 버전을 거부한다.

**대응**
- Python 3.13(또는 3.12)으로 venv를 만든다:
  ```bash
  python3.13 -m venv ~/.venvs/md-convert
  ~/.venvs/md-convert/bin/pip install 'markitdown[all]'
  ```
- 3.13이 없다면: `brew install python@3.13`.

## 3. `pydub` → ffmpeg 미설치 경고

**증상**
- stderr에 아래 경고가 나옴:
  ```
  RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
  ```
- 변환 자체(PDF/DOCX/PPTX/HTML 등)는 정상 성공, exit 0.

**원인**
- `markitdown[all]`은 오디오 전사를 위해 `pydub`를 포함하며, pydub는 ffmpeg가 없으면 import 시점에 경고를 띄운다.

**대응**
- **텍스트/문서만 변환한다면 무시해도 된다.** 호출자 스킬은 stderr 경고를 에러로 취급하지 말 것.
- 오디오(`.mp3`, `.wav` 등)를 실제로 변환할 때만 설치:
  ```bash
  brew install ffmpeg
  ```

## 4. 호출자 스킬에게 주는 권고

- `convert.py`의 **exit code만 신뢰**하라. stderr 경고는 진단 정보이며 실패 신호가 아니다.
- exit 3(미설치)을 받으면 사용자에게 설치 안내 메시지를 전달하되, **자동으로 `pip install`을 실행하지 말라** — 사용자의 Python 환경 선택(venv vs pipx vs system)을 침해하지 않기 위해서.
- exit 5(변환 실패)는 재시도하지 말고 입력을 바꾸거나 사용자에게 원인(예: 암호화 PDF)을 보고하라.

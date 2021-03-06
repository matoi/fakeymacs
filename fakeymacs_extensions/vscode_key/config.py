﻿# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## VSCode 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.vscode_target
except:
    # VSCode 用のキーバインドを利用するアプリケーションソフトを指定する
    # （ブラウザを指定した場合には、github1s.com にアクセスして開く VSCode で利用可能となります）
    fc.vscode_target  = ["Code.exe"]
    fc.vscode_target += ["chrome.exe",
                         "msedge.exe",
                         "firefox.exe"
                        ]

try:
    # 設定されているか？
    fc.vscode_prefix_key
except:
    # 置き換えするプレフィックスキーの組み合わせ（VSCode のキー、Fakeymacs のキー）を指定する（複数指定可）
    # （置き換えた Fakeymacs のプレフィックスキーを利用することにより、プレフィックスキーの後に入力する
    #   キーが全角文字で入力されることが無くなります）
    # （同じキーを指定することもできます）
    # （Fakeymacs のキーに Meta キー（M-）は指定できません）
    fc.vscode_prefix_key  = [["C-k", "C-A-k"]]

try:
    # 設定されているか？
    fc.use_ctrl_atmark_for_mark
except:
    # 日本語キーボードを利用する際、VSCode で  C-@ をマーク用のキーとして使うかどうかを指定する
    # （True: 使う、False: 使わない）
    # （VSCode で C-@ を Toggle Integrated Terminal 用のキーとして使えるようにするために設けた設定です。
    #   True に設定した場合でも、Toggle Integrated Terminal 用のキーとして  C-<半角／全角> が使えます。）
    fc.use_ctrl_atmark_for_mark = False

try:
    # 設定されているか？
    fc.use_direct_input_in_vscode_terminal
except:
    # VSCode の Terminal内 で ４つのキー（Ctrl+k、Ctrl+r、Ctrl+s、Ctrl+y）のダイレクト入力機能を使うか
    # どうかを指定する（True: 使う、False: 使わない）
    fc.use_direct_input_in_vscode_terminal = False

fakeymacs.vscode_focus = "not_terminal"
fakeymacs.rectangle_mode = False

def is_vscode_target(window):
    if window.getProcessName() in fc.vscode_target:
        return True
    else:
        return False

keymap_vscode = keymap.defineWindowKeymap(check_func=is_vscode_target)

## 共通関数
def self_insert_command4(*keys):
    func = self_insert_command(*keys)
    def _func():
        imeStatus = keymap.getWindow().getImeStatus()
        if imeStatus:
            keymap.getWindow().setImeStatus(0)
        func()
        delay()
        if imeStatus:
            keymap.getWindow().setImeStatus(1)
    return _func

def define_key3(window_keymap, keys, command):
    define_key(window_keymap, keys,
               makeKeyCommand(window_keymap, keys, command, lambda: is_vscode_target(keymap.getWindow())))

def vscodeExecuteCommand(command):
    def _func():
        self_insert_command("f1")()
        princ(command)
        self_insert_command("Enter")()
    return _func

def vscodeExecuteCommand2(command):
    def _func():
        keymap.getWindow().setImeStatus(0)
        vscodeExecuteCommand(command)()
    return _func

## カーソル移動
def previous_error():
    # VSCode Command : Go to Previous Problem in Files (Error, Warning, Info)
    self_insert_command("S-F8")()
    # vscodeExecuteCommand("GtPPiF")()
    # vscodeExecuteCommand("editor.action.marker.prevInFiles")()

def next_error():
    # VSCode Command : Go to Next Problem in Files (Error, Warning, Info)
    self_insert_command("F8")()
    # vscodeExecuteCommand("GtNPiF")()
    # vscodeExecuteCommand("editor.action.marker.nextInFiles")()

## カット / コピー
def kill_line2(repeat=1):
    if (fc.use_direct_input_in_vscode_terminal and
        fakeymacs.vscode_focus == "terminal"):
        self_insert_command("C-k")()
    else:
        kill_line(repeat)

def yank2():
    if (fc.use_direct_input_in_vscode_terminal and
        fakeymacs.vscode_focus == "terminal"):
        self_insert_command("C-y")()
    else:
        yank()

## バッファ / ウィンドウ操作
def kill_buffer():
    # github1s で動作するように、C-F4 の発行とはしていない（C-F4 がブラウザでキャッチされるため）
    # VSCode Command : View: Close Editor
    vscodeExecuteCommand("workbench.action.closeActiveEditor")()

def switch_to_buffer():
    # VSCode Command : View: Quick Open Privious Recently Used Editor in Group
    vscodeExecuteCommand("VQO-P-RUEi")()
    # vscodeExecuteCommand("workbench.action.quickOpenPreviousRecentlyUsedEditorInGroup")()

def list_buffers():
    # VSCode Command : View: Show All Editors By Most Recently Used
    vscodeExecuteCommand("VSAEBM")()
    # vscodeExecuteCommand("workbench.action.showAllEditorsByMostRecentlyUsed")()

## 文字列検索
def isearch2(direction):
    if (fc.use_direct_input_in_vscode_terminal and
        fakeymacs.vscode_focus == "terminal"):
        self_insert_command({"backward":"C-r", "forward":"C-s"}[direction])()
    else:
        isearch(direction)

def isearch_backward():
    isearch2("backward")

def isearch_forward():
    isearch2("forward")

## エディタ操作
def delete_group():
    # VSCode Command : View: Close All Editors in Group
    vscodeExecuteCommand("VCAEi")()
    # vscodeExecuteCommand("workbench.action.closeEditorsInGroup")()

def delete_other_groups():
    # VSCode Command : View: Close Editors in Other Groups
    vscodeExecuteCommand("VCEiO")()
    # vscodeExecuteCommand("workbench.action.closeEditorsInOtherGroups")()

def split_editor_below():
    # VSCode Command : View: Split Editor Orthogonal
    self_insert_command("C-k", "C-Yen")()
    # vscodeExecuteCommand("ViSEO")()
    # vscodeExecuteCommand("workbench.action.splitEditorOrthogonal")()

def split_editor_right():
    # VSCode Command : View: Split Editor
    self_insert_command("C-Yen")()
    # vscodeExecuteCommand("workbench.action.splitEditor")()

def other_group():
    # VSCode Command : View: Navigate Between Editor Groups
    vscodeExecuteCommand("VNB-EG")()
    # vscodeExecuteCommand("workbench.action.navigateEditorGroups")()

    if fc.use_direct_input_in_vscode_terminal:
        fakeymacs.vscode_focus = "not_terminal"

def switch_focus(number):
    def _func():
        # VSCode Command : View: Focus Side Bar or n-th Editor Group
        self_insert_command("C-{}".format(number))()

        if fc.use_direct_input_in_vscode_terminal:
            fakeymacs.vscode_focus = "not_terminal"
    return _func

## 矩形選択 / マルチカーソル
def mark_previous_line():
    # VSCode Command ID : cursorColumnSelectUp
    self_insert_command("C-S-A-Up")()
    # vscodeExecuteCommand("cursorColumnSelectUp")()

    fakeymacs.rectangle_mode = True

def mark_next_line():
    # VSCode Command ID : cursorColumnSelectDown
    self_insert_command("C-S-A-Down")()
    # vscodeExecuteCommand("cursorColumnSelectDown")()

    fakeymacs.rectangle_mode = True

def mark_backward_char():
    if fakeymacs.rectangle_mode:
        # VSCode Command ID : cursorColumnSelectLeft
        self_insert_command("C-S-A-Left")()
        # vscodeExecuteCommand("cursorColumnSelectLeft")()

        fakeymacs.forward_direction = False
    else:
        mark2(backward_char, False)()

def mark_forward_char():
    if fakeymacs.rectangle_mode:
        # VSCode Command ID : cursorColumnSelectRight
        self_insert_command("C-S-A-Right")()
        # vscodeExecuteCommand("cursorColumnSelectRight")()

        fakeymacs.forward_direction = True
    else:
        mark2(forward_char, True)()

def mark_backward_word():
    mark2(backward_word, False)()
    fakeymacs.rectangle_mode = False

def mark_forward_word():
    mark2(forward_word, True)()
    fakeymacs.rectangle_mode = False

def mark_beginning_of_line():
    mark2(move_beginning_of_line, False)()
    fakeymacs.rectangle_mode = False

def mark_end_of_line():
    mark2(move_end_of_line, True)()
    fakeymacs.rectangle_mode = False

def mark_next_like_this():
    # VSCode Command : Add Selection To Next Find Match
    self_insert_command("C-d")()
    # vscodeExecuteCommand("ASTN")()
    # vscodeExecuteCommand("editor.action.addSelectionToNextFindMatch")()

    fakeymacs.rectangle_mode = False
    fakeymacs.forward_direction = True

def mark_all_like_this():
    # VSCode Command : Select All Occurrences of Find Match
    self_insert_command("C-S-l")()
    # vscodeExecuteCommand("SAOo")()
    # vscodeExecuteCommand("editor.action.selectHighlights")()

    fakeymacs.rectangle_mode = False
    fakeymacs.forward_direction = True

def skip_to_previous_like_this():
    # VSCode Command : Move Last Selection To Previous Find Match
    vscodeExecuteCommand("MLSTP")()
    # vscodeExecuteCommand("editor.action.moveSelectionToPreviousFindMatch")()

    fakeymacs.rectangle_mode = False
    fakeymacs.forward_direction = True

def skip_to_next_like_this():
    # VSCode Command : Move Last Selection To Next Find Match
    self_insert_command("C-k", "C-d")()
    # vscodeExecuteCommand("MLSTN")()
    # vscodeExecuteCommand("editor.action.moveSelectionToNextFindMatch")()

    fakeymacs.rectangle_mode = False
    fakeymacs.forward_direction = True

def cursor_undo():
    if fakeymacs.is_undo_mode:
        # VSCode Command : Cursor Undo
        self_insert_command("C-u")()
        # vscodeExecuteCommand("CuUn")()
        # vscodeExecuteCommand("cursorUndo")()

        fakeymacs.rectangle_mode = False
    else:
        # VSCode Command : Cursor Redo
        vscodeExecuteCommand("CuRed")()
        # vscodeExecuteCommand("cursorRedo")()

        fakeymacs.rectangle_mode = False

def cursor_undo_switching():
    if fakeymacs.is_undo_mode:
        fakeymacs.is_undo_mode = False
    else:
        fakeymacs.is_undo_mode = True

## ターミナル操作
def create_terminal():
    # VSCode Command : Terminal: Create New Integrated Terminal
    vscodeExecuteCommand2("workbench.action.terminal.new")()

    if fc.use_direct_input_in_vscode_terminal:
        fakeymacs.vscode_focus = "terminal"

def toggle_terminal():
    if fc.use_direct_input_in_vscode_terminal:
        if fakeymacs.vscode_focus == "not_terminal":
            # VSCode Command : Terminal: Focus on Terminal View
            vscodeExecuteCommand2("terminal.focus")()

            fakeymacs.vscode_focus = "terminal"
        else:
            # VSCode Command : View: Close Panel
            vscodeExecuteCommand2("workbench.action.closePanel")()

            fakeymacs.vscode_focus = "not_terminal"
    else:
        # VSCode Command : View: Toggle Terminal
        vscodeExecuteCommand2("workbench.action.terminal.toggleTerminal")()

## その他
def execute_extended_command():
    # VSCode Command : Show All Commands
    self_insert_command3("f1")()
    # vscodeExecuteCommand("ShAlC")()
    # vscodeExecuteCommand("workbench.action.showCommands")()

def comment_dwim():
    # VSCode Command : Toggle Line Comment
    self_insert_command("C-Slash")()
    # vscodeExecuteCommand("TogLC")()
    # vscodeExecuteCommand("editor.action.commentLine")()

def trigger_suggest():
    # VSCode Command : Trigger Suggest
    self_insert_command("C-Space")()
    # vscodeExecuteCommand("TrSu")()
    # vscodeExecuteCommand("editor.action.triggerSuggest")()

## プレフィックスキーの設定
for pkey1, pkey2 in fc.vscode_prefix_key:
    define_key(keymap_vscode, pkey2, keymap.defineMultiStrokeKeymap("<VSCode> " + pkey1))

    for vkey in vkeys():
        key = "({})".format(vkey)
        for mod1 in ["", "A-"]:
            for mod2 in ["", "C-"]:
                for mod3 in ["", "S-"]:
                    mkey = mod1 + mod2 + mod3 + key
                    define_key(keymap_vscode, "{} {}".format(pkey2, mkey), self_insert_command4(pkey1, mkey))

## 「カーソル移動」のキー設定
define_key3(keymap_emacs, "M-g p",           reset_search(reset_undo(reset_counter(reset_mark(previous_error)))))
define_key3(keymap_emacs, "M-g M-p",         reset_search(reset_undo(reset_counter(reset_mark(previous_error)))))
define_key3(keymap_emacs, "M-g n",           reset_search(reset_undo(reset_counter(reset_mark(next_error)))))
define_key3(keymap_emacs, "M-g M-n",         reset_search(reset_undo(reset_counter(reset_mark(next_error)))))

if is_japanese_keyboard:
    define_key3(keymap_emacs, "Ctl-x S-Atmark",  reset_search(reset_undo(reset_counter(reset_mark(next_error)))))
else:
    define_key3(keymap_emacs, "Ctl-x BackQuote", reset_search(reset_undo(reset_counter(reset_mark(next_error)))))

## 「カット / コピー」のキー設定
define_key3(keymap_emacs, "C-k", reset_search(reset_undo(reset_counter(reset_mark(repeat3(kill_line2))))))
define_key3(keymap_emacs, "C-y", reset_search(reset_undo(reset_counter(reset_mark(repeat(yank2))))))

## 「バッファ / ウィンドウ操作」のキー設定
define_key3(keymap_emacs, "Ctl-x k",   reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key3(keymap_emacs, "Ctl-x b",   reset_search(reset_undo(reset_counter(reset_mark(switch_to_buffer)))))
define_key3(keymap_emacs, "Ctl-x C-b", reset_search(reset_undo(reset_counter(reset_mark(list_buffers)))))

## 「文字列検索」のキー設定
define_key3(keymap_emacs, "C-r", reset_undo(reset_counter(reset_mark(isearch_backward))))
define_key3(keymap_emacs, "C-s", reset_undo(reset_counter(reset_mark(isearch_forward))))

## 「エディタ操作」のキー設定
define_key3(keymap_emacs, "Ctl-x 0", reset_search(reset_undo(reset_counter(reset_mark(delete_group)))))
define_key3(keymap_emacs, "Ctl-x 1", reset_search(reset_undo(reset_counter(reset_mark(delete_other_groups)))))
define_key3(keymap_emacs, "Ctl-x 2", reset_search(reset_undo(reset_counter(reset_mark(split_editor_below)))))
define_key3(keymap_emacs, "Ctl-x 3", reset_search(reset_undo(reset_counter(reset_mark(split_editor_right)))))
define_key3(keymap_emacs, "Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_group)))))

for n in range(10):
    define_key(keymap_vscode, "C-A-{}".format(n), reset_search(reset_undo(reset_counter(reset_mark(switch_focus(n))))))
    if not fc.use_ctrl_digit_key_for_digit_argument:
        define_key(keymap_vscode, "C-{}".format(n), reset_search(reset_undo(reset_counter(reset_mark(switch_focus(n))))))

## 「矩形選択 / マルチカーソル」のキー設定
define_key(keymap_vscode, "C-A-p",   reset_search(reset_undo(reset_counter(repeat(mark_previous_line)))))
define_key(keymap_vscode, "C-A-n",   reset_search(reset_undo(reset_counter(repeat(mark_next_line)))))
define_key(keymap_vscode, "C-A-b",   reset_search(reset_undo(reset_counter(repeat(mark_backward_char)))))
define_key(keymap_vscode, "C-A-f",   reset_search(reset_undo(reset_counter(repeat(mark_forward_char)))))
define_key(keymap_vscode, "C-A-S-b", reset_search(reset_undo(reset_counter(repeat(mark_backward_word)))))
define_key(keymap_vscode, "C-A-S-f", reset_search(reset_undo(reset_counter(repeat(mark_forward_word)))))
define_key(keymap_vscode, "C-A-a",   reset_search(reset_undo(reset_counter(mark_beginning_of_line))))
define_key(keymap_vscode, "C-A-e",   reset_search(reset_undo(reset_counter(mark_end_of_line))))
define_key(keymap_vscode, "C-A-d",   reset_search(reset_undo(reset_counter(mark_next_like_this))))
define_key(keymap_vscode, "C-A-S-d", reset_search(reset_undo(reset_counter(mark_all_like_this))))
define_key(keymap_vscode, "C-A-r",   reset_search(reset_undo(reset_counter(skip_to_previous_like_this))))
define_key(keymap_vscode, "C-A-s",   reset_search(reset_undo(reset_counter(skip_to_next_like_this))))
define_key(keymap_vscode, "C-A-u",   reset_search(reset_counter(cursor_undo)))
define_key(keymap_vscode, "C-A-g",   reset_search(reset_counter(cursor_undo_switching)))

## 「ターミナル操作」のキー設定
define_key(keymap_vscode, "C-S-(243)", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
define_key(keymap_vscode, "C-S-(244)", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
define_key(keymap_vscode, "C-(243)",   reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))
define_key(keymap_vscode, "C-(244)",   reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))

if is_japanese_keyboard:
    define_key(keymap_vscode, "C-S-Atmark", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
    if not fc.use_ctrl_atmark_for_mark:
        define_key(keymap_vscode, "C-Atmark", reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))
else:
    define_key(keymap_vscode, "C-S-BackQuote", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
    define_key(keymap_vscode, "C-BackQuote",   reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))

## 「その他」のキー設定
define_key3(keymap_emacs, "M-x",         reset_search(reset_undo(reset_counter(reset_mark(execute_extended_command)))))
define_key3(keymap_emacs, "M-Semicolon", reset_search(reset_undo(reset_counter(comment_dwim))))

if is_japanese_keyboard:
    define_key(keymap_vscode, "C-Colon", trigger_suggest)
else:
    define_key(keymap_vscode, "C-Quote", trigger_suggest)

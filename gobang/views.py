from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from gobang.src.gobang_board import Gobang
from gobang.src.common import generate_random_hash
from time import time

board_dict = {}


def index(request):
    context = {"today": datetime.now() + timedelta(hours=9)}
    return render(request, "index.html", context)


def show_board(request):
    global board_dict
    now = time()
    # 10分以上操作されてないkeyは削除する
    board_dict = {k: v for k, v in board_dict.items() if now - v["last_update"] <= 600}
    if "board_number" in request.session:
        key = request.session.get("board_number")
        if key in board_dict:
            board_dict[key]["board"].reset()
        else:
            board_dict[key] = {"last_update": time(), "board": Gobang()}
    else:
        board_number = generate_random_hash()
        request.session["board_number"] = board_number
        gobang_agent = Gobang()
        board_dict[board_number] = {"last_update": time(), "board": gobang_agent}
    return render(request, 'board.html')


@csrf_exempt
def put_stone(request):
    if request.method == "POST":
        gobang_agent_number = request.session.get("board_number")
        if gobang_agent_number not in board_dict:
            data = {"message": "10分以上操作されていない為セッションが切れています。", "success": False}
        else:
            gobang_agent = board_dict[gobang_agent_number]["board"]
            y, x, strong = int(request.POST.get("y")), int(request.POST.get("x")), request.POST.get("strong")
            gobang_agent.put(y, x, strong)
            data = {'message': '', "success": True}
            board_dict[gobang_agent_number]["last_update"] = time()
        return JsonResponse(data)
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})


def observe(request):
    gobang_agent_number = request.session.get("board_number")
    if gobang_agent_number not in board_dict:
        data = {"message": "10分以上操作されていない為セッションが切れています。", "success": False}
        return JsonResponse(data)
    gobang_agent = board_dict[gobang_agent_number]["board"]
    board = gobang_agent.observe()
    wins = gobang_agent.wins
    if sum(wins) == 2:
        winner = "黒" if gobang_agent.turn == gobang_agent.black else "白"
        message = f"2人とも5目が成立していますが、観測者が{winner}のため{winner}の勝ちです。"
    elif not sum(wins):
        message = "勝負はついていません"
    else:
        winner = "黒" if wins[0] else "白"
        message = f"{winner}の勝ちです。"
    gobang_agent.reset_wins()
    board_dict[gobang_agent_number]["last_update"] = time()
    return JsonResponse({"board": board.tolist(), "message": message, "success": True})


def reset(request):
    gobang_agent_number = request.session.get("board_number")
    if gobang_agent_number in board_dict:
        board_dict[gobang_agent_number]["board"].reset()
        board_dict[gobang_agent_number]["last_update"] = time()
    else:
        board_dict[gobang_agent_number] = {"last_update": time(), "board": Gobang()}
    return JsonResponse({"message": "成功"})

from django.shortcuts import render
from gobang.src.gobang_board import Gobang
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

gobang_agent = Gobang()


def index(request):
    context = {"today": datetime.now()}
    return render(request, "index.html", context)


def show_board(request):
    return render(request, 'board.html')


@csrf_exempt
def put_stone(request):
    if request.method == "POST":
        y, x, strong = int(request.POST.get("y")), int(request.POST.get("x")), request.POST.get("strong")
        gobang_agent.put(y, x, strong)
        data = {'message': '大成功'}
        print("yahoo")
        return JsonResponse(data)
    else:
        return JsonResponse({'message': 'This endpoint only accepts POST requests'})


def observe(request):
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
    return JsonResponse({"board": board.tolist(), "message": message})


def reset(request):
    gobang_agent.reset()
    return JsonResponse({"message": "成功"})

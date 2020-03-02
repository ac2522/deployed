from django.shortcuts import render
from django.utils.safestring import mark_safe

from portfolio.models import Chess_board
import json


def home(request):
	if 'alexcarter' in request.COOKIES:
		return render(request, 'home.html', {})
	else:
		board = Chess_board()
		data = mark_safe(json.dumps(board.rep))
		data2 = mark_safe(json.dumps(board.moves))
		data3 = mark_safe(json.dumps(board.mate_moves))
		return render(request, 'login.html',{'board': data, "moves": data2, "mates": data3})
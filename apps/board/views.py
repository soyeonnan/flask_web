from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from apps.board.forms import WriteBoardForm
from apps.app import db
from apps.board.models import Board

bp = Blueprint(
  "board",
  __name__,
  template_folder="templates",
  static_folder="static"
)

@bp.route('/')
def index():
  page = request.args.get('page', type=int, default=1) # default : 페이지 뭘 안 적으면 걍 1로 처리해라~

  boards = Board.query.order_by(Board.created_at.desc()) # .all을 하면 쿼리문이 실행 or 뗀 거는 쿼리 객체임

  # paginate함수는 페이징 처리가 완료 된 pagination 객체가 리턴
  # items : 레코드들, total : 전체 레코드 수, per_page : 페이지 당 나타 낼 레코드 수
  # page : 현재 페이지, prev_num : 이전 페이지 번호, next_num : 다음 페이지 번호
  # has_prev : 이전 페이지 여부, has_next : 다음 페이지 여부 
  boards = boards.paginate(page=page, per_page=10)

  return render_template('board/index.html', boards=boards)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_board():
  form = WriteBoardForm()

  if form.validate_on_submit():
    board = Board(
      subject = form.subject.data,
      content = form.content.data,
      user_id = current_user.id
    )

    db.session.add(board)
    db.session.commit()
    return redirect(url_for('board.index'))

  return render_template('board/write.html', form=form)

@bp.route('/detail/<int:board_id>')
def detail(board_id):
  board = Board.query.get_or_404(board_id)

  return render_template('board/detail.html', board=board)

@bp.route('/edit/<board_id>', methods=['GET', 'POST'])
def edit(board_id):
  board = Board.query.get_or_404(board_id)
  form = WriteBoardForm(obj = board)

  if form.validate_on_submit():
    board.subject = form.subject.data
    board.content = form.content.data

    db.session.add(board)
    db.session.commit()

    return redirect(url_for('board.index'))
  
  return render_template('board/edit.html', form=form, board=board)


@bp.route('/delete/<board_id>')
def delete(board_id):
  board = Board.query.get(board_id)
  db.session.delete(board)
  db.session.commit()

  return redirect(url_for('board.index'))

# @bp.route('/dummy') -> 이거 했더니 게시물 쫘르륵 생김
# def make_dummy():
#   for i in range(300):
#     board = Board(
#       subject = f"임시 제목 - {i}",
#       content = f"임시 내용 - {i}",
#       user_id = 2
#     )

#     db.session.add(board)
#     db.session.commit() 

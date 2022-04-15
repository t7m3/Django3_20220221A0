from asyncio.log import logger
from cmath import log
from email import message
from tabnanny import check
from tokenize import group
from urllib import request
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Message, Friend, Group, Good
from .forms import GroupCheckForm, GroupSelectForm, \
    FriendsForm, CreateGroupForm, PostForm 

# index のビュー関数
@login_required(login_url='/admin/login')
def index(request, page=1):
    print('＊＊＊＊＊通過(index0)')  # デバグ用
    # publicのuserを取得
    (public_user, public_group) = get_public()

    print('＊＊＊＊＊その時 request.method=',request.method)  # デバグ用
    # POST送信時の処理
    if request.method == 'POST':
        print('＊＊＊＊＊通過(index1)')  # デバグ用
        # Groupのチェックを更新したときの処理
        # フォームの用意
        checkform = GroupCheckForm(request.user, request.POST)
        # チェックされたGroup名をリストにまとめる
        glist = []
        for item in request.POST.getlist('groups'):
            glist.append(item)
        print('＊＊＊＊＊通過(index11)')  # デバグ用
        print('＊＊＊＊＊その時 glist=',glist)  # デバグ用
        # Messageの取得
        messages = get_your_group_message(request.user, glist, page)

    # GETアクセス時の処理
    else:
        print('＊＊＊＊＊通過(index20)')  # デバグ用
        print('＊＊＊＊＊その時 request.user=',request.user)  # デバグ用
        # フォームの用意
        checkform = GroupCheckForm(request.user)

        # Groupのリストを取得
        gps = Group.objects.filter(owner=request.user)
        glist = [public_group.title]
        for item in gps:
            glist.append(item.title)
            print('＊＊＊＊＊通過(index21)')  # デバグ用
            print('＊＊＊＊＊その時 glist=',glist)  # デバグ用
        
        # メッセージの取得
        messages = get_your_group_message(request.user, glist, page)

    # 共通処理
    params = {
        'login_user':request.user,
        'contents':messages,
        'check_form':checkform,
    }
    print('＊＊＊＊＊通過(index9)')  # デバグ用
    return render(request, 'sns/index.html', params)


# Groupの処理
@login_required(login_url='/admin/login/')
def groups(request):

    print('＊＊＊＊＊通過(groups0)')  # デバグ用
    print('＊＊＊＊＊その時 request.method=',request.method)  # デバグ用  
    # 自分が登録したFriendを取得
    friends = Friend.objects.filter(owner=request.user)

    # POST送信時の処理
    if request.method == 'POST':
        print('＊＊＊＊＊通過(groups1)')  # デバグ用
        print('＊＊＊＊＊その時 request.POST[mode]=',request.POST['mode'])  # デバグ用

        # Groupsメニュー選択肢の処理
        if request.POST['mode'] == '__groups_form__':
            print('＊＊＊＊＊通過(groups11)')  # デバグ用

            # 選択したgroup名を取得
            sel_group = request.POST['groups'] 
            # Groupを取得
            gp = Group.objects.filter(owner=request.user) \
                .filter(title=sel_group).first()
            # Groupに含まれるFriendを取得
            fds = Friend.objects.filter(owner=request.user) \
                .filter(group=gp)
            print('＊＊＊＊＊通過(groups12)')  # デバグ用
            print('＊＊＊＊＊その時 Friend.objects.filter(owner=request.user=', \
                Friend.objects.filter(owner=request.user))  # デバグ用に一部変更 2020-4-6
            # FriendのUserをリストにまとめる
            vlist = []
            for item in fds:
                vlist.append(item.user.username)
            print('＊＊＊＊＊通過(groups13)')  # デバグ用
            print('＊＊＊＊＊その時 vlist=',vlist)  # デバグ用
            # フォームの用意
            groupsform = GroupSelectForm(request.user, request.POST)
            friendsform = FriendsForm(request.user, friends=friends, vals=vlist)

        # Friendsのチェック更新時の処理
        if request.POST['mode'] == '__friends_form__':
            print('＊＊＊＊＊通過(groups12)')  # デバグ用

            # 選択したGroupの取得
            sel_group = request.POST['group']  # なぜ group？ GroupSelectFormではself.fields['groups']なのに。
            group_obj = Group.objects.filter(title=sel_group).first()
            print(group_obj)
            # チェックしたFriendsを取得
            # ・・・というよりも、チェック(選択)したメンバーの取得なのでは。Friendsはmodel(テーブル)なのでは。そこが紛らわしい。
            sel_fds = request.POST.getlist('friends')  # こっちは、ちゃんと friends になっているね。
            # FriendsのUserを取得
            # ・・・チェック(選択)したメンバーのUserクラスのインスタンス(レコード)を取得、なのでは。
            sel_users = User.objects.filter(username__in=sel_fds)
            # Userのリストに含まれるユーザーが登録したFriendを取得
            # ・・・model(テーブル)のFriendから、選択されたメンバーのレコードを取得、なのでは。ownerはrequest.userで。
            fds = Friend.objects.filter(owner=request.user) \
                    .filter(user__in=sel_users)
            # すべてのFriendにGroupを設定し保存する。
            vlist = []
            for item in fds:
                item.group = group_obj  # ←このような処理なので、ある1人のユーザーに対して、別のある1人のユーザーが所属できるるグループはひとつだけかな？
                item.save()             # 　→そんな気がします。
                vlist.append(item.user.username)
            # メッセージを設定
            messages.success(request, ' チェックされたFriendを' + sel_group + 'に登録しました。')
            # フォームの用意
            groupsform = GroupSelectForm(request.user, {'groups':sel_group})
            friendsform = FriendsForm(request.user, friends=friends, vals=vlist)

    # GETアクセス時の処理
    else:
        print('＊＊＊＊＊通過(groups2)')  # デバグ用

        # フォームの用意
        groupsform = GroupSelectForm(request.user)
        friendsform = FriendsForm(request.user, friends=friends, vals=[])
        sel_group = '-'

    print('＊＊＊＊＊通過(groups3)')  # デバグ用
    print('＊＊＊＊＊その時 friends=',friends)  # デバグ用
    # 共通処理
    createform = CreateGroupForm()
    params = {
        'login_user':request.user,
        'groups_form':groupsform,
        'friends_form':friendsform,
        'create_form':createform,
        'group':sel_group
    }
    print('＊＊＊＊＊通過(groups4)')  # デバグ用
    return render(request, 'sns/groups.html', params)


# Friendの追加処理
@login_required(login_url='/admin/login/')
def add(request):
    print('＊＊＊＊＊通過(add0)')  # デバグ用
    # 追加するUserを取得
    add_name = request.GET['name']
    add_user = User.objects.filter(username=add_name).first()

    print('＊＊＊＊＊通過(add1)')  # デバグ用
    print('＊＊＊＊＊その時 add_name=',add_name)  # デバグ用
    print('＊＊＊＊＊その時 add_user=',add_user)  # デバグ用
    print('＊＊＊＊＊その時 request.user=',request.user)  # デバグ用
    # Userが本人だった場合の処理
    if add_user == request.user:
        print('＊＊＊＊＊通過(add11)')  # デバグ用
        messages.info(request, "自分自身をFriendに追加することはできません。")
        # a = input("ここでいったん止めたい。何か入力してください：")  # デバグ用
        return redirect(to='/sns')
    
    print('＊＊＊＊＊通過(add2)')  # デバグ用
    # publicの取得
    (public_user, pubulic_group) = get_public()

    print('＊＊＊＊＊通過(add3)')  # デバグ用
    # add_userのFriendの数を調べる
    frd_num = Friend.objects.filter(owner=request.user) \
            .filter(user=add_user).count()
    
    print('＊＊＊＊＊通過(add4)')  # デバグ用
    # ゼロより大きければ既に登録済み
    if frd_num > 0:
        messages.info(request, add_user.username + \
                '　は既に追加されています。')
        return redirect(to='/sns')

    print('＊＊＊＊＊通過(add5)')  # デバグ用
    # ここからFriendの登録処理
    frd = Friend()
    frd.owner = request.user
    frd.user = add_user
    frd.group = pubulic_group
    frd.save()
    # メッセージを設定
    messages.success(request, add_user.username + 'を追加しました！ \
            groupページに移動して、追加したFriendをメンバーに設定してください。')
    return redirect(to='/sns')


# グループの作成処理
@login_required(login_url='/admin/login')
def creategroup(request):
    print('＊＊＊＊＊通過(creategroup0)')  # デバグ用
    # # Groupを作り、Userとtitleを設定して保存する
    gp = Group()
    gp.owner = request.user
    gp.title = request.user.username + 'の' + request.POST['group_name']
    gp.save()
    messages.info(request, '新しいグループを作成しました。')
    return redirect(to='/sns/groups')


# メッセージのポスト処理
@login_required(login_url='/admin/login')
def post(request):
    print('＊＊＊＊＊通過(post0)')  # デバグ用
    print('*****出力_def post(request): 先頭')
    #POST送信の処理
    if request.method == 'POST':
        # 送信内容の取得
        gr_name = request.POST['groups']
        content = request.POST['content']
        # Groupの取得
        group = Group.objects.filter(owner=request.user).filter(title=gr_name).first()
        if group == None:
            (pub_user, group) = get_public()
        msg = Message()
        msg.owner = request.user
        msg.group = group
        msg.content = content
        msg.save()
        # メッセージを設定
        messages.success(request, '新しいメッセージを投稿しました！')
        return redirect(to='/sns')

    # GETアクセス時の処理
    else:
        form = PostForm(request.user)

    # 共通処理
    params = {
        'login_user':request.user,
        'form':form
    }
    print('*****出力_def post(request): GETアクセス時の処理')
    return render(request, 'sns/post.html', params)


# 投稿をシェアする
@login_required(login_url='/admin/login')
def share(request, share_id):
    # シェアするMessageの取得
    share = Message.objects.get(id=share_id)
    print(share)

    #POST送信時の処理
    if request.method == 'POST':
        # 送信内容を取得
        gr_name = request.POST['groups']
        content = request.POST['content']
        # Groupの取得
        group = Group.objects.filter(owner=request.user) \
                .filter(title=gr_name).first()
        if group == None:
            (pub_user, group) = get_public()
        # メッセージを作成し、設定をして保存
        msg = Message()
        msg.owner = request.user
        msg.group = group
        msg.content = content
        msg.share_id = share_id
        msg.save()

        share_msg = msg.get_share()
        share_msg.share_count += 1
        share_msg.save()

        # メッセージを設定
        messages.success(request, 'メッセージをシェアしました！')
        return redirect(to='/sns')

    # 共通処理
    form = PostForm(request.user)
    params = {
        'login_user':request.user,
        'form':form,
        'share':share,
    }
    return render(request, 'sns/share.html', params)


# goodボタンの処理
@login_required(login_url='/admin/login')
def good(request, good_id):
    # goodするMessageを取得
    good_msg = Message.objects.get(id=good_id)
    # 自分がメッセージにGoodした数を調べる
    is_good = Good.objects.filter(owner=request.user) \
            .filter(message=good_msg).count()
    # ゼロより大きければgood済み
    if is_good > 0:
        messages.success(request, '既にメッセージはGoodしています。')
        return redirect(to='/sns')

    # Messageのgood_countを１増やす
    good_msg.good_count += 1
    good_msg.save()

    # Goodを作成し、設定して保存
    good = Good()
    good.owner = request.user
    good.message = good_msg
    good.save()

    # メッセージを設定
    messages.success(request, 'メッセージにGoodしました！')
    return redirect(to='/sns')



# これ以降は普通の関数======================

# 指定されたグループおよび検索文字によるMessagaの取得
def get_your_group_message(owner, glist, page):
    page_num = 10 #ページあたりの表示数
    # publicの取得
    (public_user, public_group) = get_public()
    # チェックされたGroupの取得
    groups = Group.objects.filter(Q(owner=owner) \
        |Q(owner=public_user)).filter(title__in=glist)
    # Groupに含まれるFriendの取得
    me_friends = Friend.objects.filter(group__in=groups)
    # Friendのuserをリストにまとめる
    me_users = []
    for f in me_friends:
        me_users.append(f.user)
    # UserリストのUserが作ったGroupの取得
    his_groups = Group.objects.filter(owner__in=me_users)
    his_friends = Friend.objects.filter(user=owner) \
        .filter(group__in=his_groups)
    me_groups = []
    for hf in his_friends:
        me_groups.append(hf.group)
    # groupがgroupsに含まれるか、me_groupsに含まれるMessageの取得
    messages = Message.objects.filter(Q(group__in=groups) \
        |Q(group__in=me_groups))
    # ページネーションで指定ページを取得
    page_item = Paginator(messages, page_num)
    
    return page_item.get_page(page)


# publicなUserとGroupを取得する
def get_public():
    public_user = User.objects.filter(username='public').first()
    public_group = Group.objects.filter(owner=public_user).first()
    return (public_user, public_group)

from flask import Flask, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Oturum için gerekli anahtar

@app.route('/')
def hello_world():
    return """
    <p>Hello,World!</p> <br>
    <a href='/facts'>Rastgele bir gerçek için tıkla</a><br>
    <a href='/russian_roulette'>Rus Ruleti Oyna</a>
    """

@app.route('/facts')
def facts():
    facts_list = [
        "Teknolojik bağımlılıktan mustarip olan çoğu kişi, kendilerini şebeke kapsama alanı dışında bulduklarında veya cihazlarını kullanamadıkları zaman yoğun stres yaşarlar.","2018 yılında yapılan bir araştırmaya göre 18-34 yaş arası kişilerin %50'den fazlası kendilerini akıllı telefonlarına bağımlı olarak görüyor.","Teknolojik bağımlılık çalışması, modern bilimsel araştırmanın en ilgili alanlarından biridir.","2019'da yapılan bir araştırmaya göre, insanların %60'ından fazlası akıllı telefonlarındaki iş mesajlarına işten ayrıldıktan sonraki 15 dakika içinde yanıt veriyor."
    ]
    return f'<p>{random.choice(facts_list)}</p>'

@app.route('/russian_roulette')
def russian_roulette():
    # Oyun başlatılırken veya eski session hatalıysa sıfırla
    if 'game' not in session or not isinstance(session['game'], dict) or 'history' not in session['game']:
        chambers = [0]*6
        bullets = random.randint(1, 5)
        for i in range(bullets):
            chambers[i] = 1
        random.shuffle(chambers)
        session['game'] = {
            'chambers': chambers,
            'index': 0,
            'over': False,
            'message': 'Oyun başladı! Sıra sende.',
            'history': []
        }
    game = session['game']

    target = request.args.get('target')

    if target in ['self', 'bot'] and not game['over'] and game['index'] < 6:
        # Kullanıcı seçimi
        if target == 'self':
            if game['chambers'][game['index']] == 1:
                game['over'] = True
                game['message'] = 'BAM! Kendini vurdun. Kaybettin!'
                game['history'].append('Sen kendini vurdun!')
            else:
                game['message'] = 'Tık! Hayattasın. Şimdi botun sırası.'
                game['history'].append('Sen kendini vurdun, hayattasın.')
                game['index'] += 1
                # Botun sırası
                if game['index'] < 6 and not game['over']:
                    bot_choice = random.choice(['self', 'user'])
                    if bot_choice == 'self':
                        if game['chambers'][game['index']] == 1:
                            game['over'] = True
                            game['message'] = 'Bot kendini vurdu ve öldü. Kazandın!'
                            game['history'].append('Bot kendini vurdu ve öldü!')
                        else:
                            game['message'] = 'Bot kendini vurdu, hayatta. Şimdi senin sıran.'
                            game['history'].append('Bot kendini vurdu, hayatta.')
                            game['index'] += 1
                    else:
                        if game['chambers'][game['index']] == 1:
                            game['over'] = True
                            game['message'] = 'Bot seni vurdu! Kaybettin!'
                            game['history'].append('Bot seni vurdu!')
                        else:
                            game['message'] = 'Bot seni vurdu ama hayattasın. Şimdi senin sıran.'
                            game['history'].append('Bot seni vurdu ama hayattasın.')
                            game['index'] += 1
        elif target == 'bot':
            if game['chambers'][game['index']] == 1:
                game['over'] = True
                game['message'] = 'BAM! Karşıdakini vurdun. Kazandın!'
                game['history'].append('Sen botu vurdun!')
            else:
                game['message'] = 'Tık! Bot hayatta. Şimdi botun sırası.'
                game['history'].append('Sen botu vurdun, bot hayatta.')
                game['index'] += 1
                # Botun sırası
                if game['index'] < 6 and not game['over']:
                    bot_choice = random.choice(['self', 'user'])
                    if bot_choice == 'self':
                        if game['chambers'][game['index']] == 1:
                            game['over'] = True
                            game['message'] = 'Bot kendini vurdu ve öldü. Kazandın!'
                            game['history'].append('Bot kendini vurdu ve öldü!')
                        else:
                            game['message'] = 'Bot kendini vurdu, hayatta. Şimdi senin sıran.'
                            game['history'].append('Bot kendini vurdu, hayatta.')
                            game['index'] += 1
                    else:
                        if game['chambers'][game['index']] == 1:
                            game['over'] = True
                            game['message'] = 'Bot seni vurdu! Kaybettin!'
                            game['history'].append('Bot seni vurdu!')
                        else:
                            game['message'] = 'Bot seni vurdu ama hayattasın. Şimdi senin sıran.'
                            game['history'].append('Bot seni vurdu ama hayattasın.')
                            game['index'] += 1
        session['game'] = game
        return redirect(url_for('russian_roulette'))

    html = f"""
    <h2>Rus Ruleti</h2>
    <p>{game['message']}</p>
    <p>Kalan yuva: {6 - game['index']}</p>
    <ul>
        {''.join(f'<li>{h}</li>' for h in game.get('history', []))}
    </ul>
    <form method='get' style='display:flex; gap:10px;'>
        {'<button type="submit" name="target" value="self">Kendini Vur</button>' if not game['over'] and game['index'] < 6 else ''}
        {'<button type="submit" name="target" value="bot">Karşıdakini Vur</button>' if not game['over'] and game['index'] < 6 else ''}
    </form>
    <form method='post' action='/russian_roulette_reset'>
        <button type='submit'>Yeniden Başlat</button>
    </form>
    <a href='/'>Ana Sayfa</a>
    """
    return html

@app.route('/russian_roulette_reset', methods=['POST'])
def russian_roulette_reset():
    session.pop('game', None)
    return redirect(url_for('russian_roulette'))

    

app.run(debug=True)
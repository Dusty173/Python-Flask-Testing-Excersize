class BoggleGame {
    constructor(boardId, secs = 60){
        this.secs = secs;
        this.board = $('#' + boardId);
        this.words = new  Set();
        this.score = 0;
        this.displayTime();
        this.timer = setInterval(this.tick.bind(this), 1000);
        $('.submit-word', this.board).on('submit', this.handleSubmit.bind(this));
    }   

    displayWord(word){
        $('.words', this.board).append($('<li>', {text : word}));
    }

    displayScore(){
        $('.cur-score', this.board).text(this.score)
    }

    displayMsg(msg,cls){
        $('.msg', this.board).text(msg).removeClass().addClass(`msg ${cls}`);
    }

    async handleSubmit(e){
        e.preventDefault();
        const $word = $('.word', this.board);
        let word = $word.val()
        
        if(!word) return;
        if(this.words.has(word)){
            this.displayMsg(`You already found ${word}`, 'err');
            return;
        }

        const res = await axios.get('/verify-word', {params: {word : word}});
        if(res.data.result === 'not-word'){
            this.displayMsg(`${word} is not an English word`, 'err');
        } else if(res.data.result === 'not-on-board'){
            this.displayMsg(`${word} is not on this board`, 'err');
        } else {
            this.displayWord(word);
            this.score += word.length;
            this.displayScore();
            this.words.add(word);
            this.displayMsg(`Added: ${word}`, 'ok')
        }
        $word.val('').focus()
    }
    
    displayTime(){
        $('.timer', this.board).text(this.secs);
    }

    async tick() {
        this.secs -= 1;
        this.displayTime();

        if(this.secs === 0){
            clearInterval(this.timer);
            await this.finalScore()
        }
    }

    async finalScore(){
        $('.submit-word', this.board).hide();
        const res = await axios.post('/post-score', {score : this.score});
        if(res.data.brokeRecord){
            this.displayMsg(`New High Score! ${this.score}`, 'ok');
        } else {
            this.displayMsg(`Final Score: ${this.score}`, 'ok')
        }
    }

}
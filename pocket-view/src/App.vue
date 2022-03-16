<template>
  <div>
    <div v-if="state.pokemonData == null || state.pokemonDataDetail == null">
      ロード中...
    </div>
    <div v-if="state.pokemonData != null && state.pokemonDataDetail != null">
      <h1>ポケモン逆紅Wordle</h1>
      <h3>遊び方</h3>
      このポケモンは何か当てよう！回答欄にはひらがなで入力してね。<br/>
      最初は間違っても大丈夫!8回まで答えられるよ。<br/>
      間違うたびにヒントが増えていくから、わからなかったら適当な文字をいれてみるのも戦略だ！
      <hr/>
      <h3>難易度(下のボタンで変更できるよ)</h3>
      <div>今の設定:{{state.sedai}}まで</div>
      <button  v-on:click="changeDefficulty(151, '赤緑世代')">赤緑世代</button>
      <button v-on:click="changeDefficulty(251, '金銀世代')">金銀世代</button>
      <button v-on:click="changeDefficulty(386, 'ルビサファ世代')">ルビサファ世代</button>
      <button v-on:click="changeDefficulty(493, 'ダイパ世代')">ダイパ世代</button>
      <button v-on:click="changeDefficulty(807, 'サンムーン世代q')">サンムーン世代</button>
      <button v-on:click="changeDefficulty(null, '最新')">最新まで</button>
      <hr/>
      <div>
        <div v-if="clearCheck() == 'success'">
          <h1>正解や！</h1>
        </div>
        <div v-if="clearCheck() == 'failed'">
          <h1>失敗や!</h1>
        </div>
        <div v-if="clearCheck() != ''">  
          <img :src="state.pokemonData.sprites_front_default"/>
          <img :src="state.pokemonData.sprites_back_default"/>
        </div>
        <div v-if="clearCheck() == ''">  ヒント1</div>
        <p  v-if="state.pokemonData.stats != null">H: {{state.pokemonData["stats"]["h"]}}</p>
        <p  v-if="state.pokemonData.stats != null">A: {{state.pokemonData["stats"]["a"]}}</p>
        <p  v-if="state.pokemonData.stats != null">B: {{state.pokemonData["stats"]["b"]}}</p>
        <p  v-if="state.pokemonData.stats != null">C: {{state.pokemonData["stats"]["c"]}}</p>
        <p  v-if="state.pokemonData.stats != null">D: {{state.pokemonData["stats"]["d"]}}</p>
        <p  v-if="state.pokemonData.stats != null">S: {{state.pokemonData["stats"]["s"]}}</p>
      </div>
      <div v-if="clearCheck() != ''">  
        <p  v-if="state.pokemonDataDetail.name != null">{{ state.pokemonDataDetail.name }}</p>
        <p  v-if="state.pokemonDataDetail.name != null">{{ state.pokemonDataDetail.flavor_text_entry }}</p>
        <p  v-if="state.pokemonDataDetail.name != null">{{ state.pokemonDataDetail.flavor_text_entry_ja }}</p>
      </div>
      <div v-if="clearCheck() == ''">  
        <div>ヒント2</div>
        {{getQuestion()}}
      </div>

      <div>回答欄(ひらがな または 記号(♂♀ー・：))</div>
      <input v-model="state.input_answer" :placeholder="getPlaceHolder()" :maxlength="state.pokemonDataDetail.name.length">
      <button v-if="clearCheck() == ''" v-on:click="executeAnswer()">回答する</button>
      回答回数: {{state.count}}/{{state.maxCount}}
      <hr/>
      <div v-if="clearCheck() == ''">  
        <div>チェックリスト(赤色は答えに含まれる)</div>
          <div v-for="value in getAnsweredTaiou()" v-bind:key="value">
            <div v-for="arr in value" v-bind:key="arr" class="inline-list">
              <div v-for="l in arr" v-bind:key="l" class="inline-list"> 
                <label v-if="state.pokemonDataDetail.name_hira.includes(l)" class="isMatch">{{l}}</label> 
                <label v-if="!state.pokemonDataDetail.name_hira.includes(l)">{{l}}</label> 
              </div>
            </div>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, reactive } from 'vue'
import axios from 'axios'
import { defineComponent } from "@vue/composition-api";

export default defineComponent({
  name: 'App',  
  setup() {
    const state = reactive({
      pokemonData: null,
      pokemonDataDetail: null,
      input_answer: '',
      answer: '',
      answeredLetter: new Set(),
      count: 0,
      maxCount: 8,
      sedai: '最新'
    })

    async function getPokemon(maxId) {
      const url = maxId == null ? 'https://18j6btujfb.execute-api.ap-northeast-1.amazonaws.com/api/random' : `https://18j6btujfb.execute-api.ap-northeast-1.amazonaws.com/api/random?max_id=${maxId}`
      const response = await axios.get(url)
      state.pokemonData = response.data
      
      console.log(state.pokemonData)
      const responseDetail = await axios.get('https://18j6btujfb.execute-api.ap-northeast-1.amazonaws.com/api/detail?id=' + state.pokemonData.id)
      state.pokemonDataDetail = responseDetail.data
    }
      
    function getPlaceHolder() {
      return `${state.pokemonDataDetail.name.length}文字`
    }

    function executeAnswer() {
      const matched = state.input_answer.match("^[ぁ-ん♂♀ー・：ゔ]*$");
      if (matched == null || state.input_answer.length != state.pokemonDataDetail.name.length) {
        alert(`ひらがなか記号(♂♀ー・：)の${state.pokemonDataDetail.name.length}文字じゃないよ。`)
        return;
      }
      state.answer = state.input_answer
      state.input_answer.split('').forEach(l => {
        state.answeredLetter.add(l)
        taiou(l).forEach(arr => arr.forEach(taiouLetter => state.answeredLetter.add(taiouLetter)))
      })
      state.count += 1
    }

    function clearCheck() {
      if (state.answer ==  state.pokemonDataDetail.name_hira) {
        return 'success';
      }
      if (state.count >= state.maxCount) {
        return 'failed';
      }
      return ''
    }

    function getQuestion() {
      return state.pokemonDataDetail.flavor_text_entry.split('')
          .map(l => {
            if (l.match("^[ぁ-んー]*$") == null || l == "。"|| state.answeredLetter.has(l)) {
              return l;
            }
            return "■"
          })
          .join('')
    }

    function taiou(str) {
      const taiouList = [
        ["あ", "あ", "ぁ"],
        ["い", "い", "ぃ"],
        ["う", "う", "ぅ", "ゔ"],
        ["え", "え", "ぇ"],
        ["お", "お", "ぉ"],
        ["か", "が"],
        ["き", "ぎ"],
        ["く", "ぐ"],
        ["け", "げ"],
        ["こ", "ご"],
        ["さ", "ざ"],
        ["し", "じ"],
        ["す", "ず"],
        ["せ", "ぜ"],
        ["そ", "ぞ"],
        ["た", "だ"],
        ["ち", "ぢ"],
        ["つ", "づ", "っ"],
        ["て", "で"],
        ["と", "ど"],
        ["は", "ば", "ぱ"],
        ["ひ", "び", "ぴ"],
        ["ふ", "ぶ", "ぷ"],
        ["へ", "べ", "ぺ"],
        ["ほ", "ぼ", "ぽ"],
        ["や", "ゃ"],
        ["ゆ", "ゅ"],
        ["よ", "ょ"],  
      ]
      return taiouList
        .filter(taiouArray => taiouArray.includes(str))
    }

    function getAnsweredTaiou() {
      const aiueoList = [
        ["あいうえお"],
        ["かきくけこ"],
        ["さしすせそ"],
        ["たちつてと"],
        ["なにぬねの"],
        ["はひふへほ"],
        ["まみむめも"],
        ["や　ゆ　よ"],
        ["らりるれろ"],
        ["わ　を　ん"],

        ["がぎぐげご"],
        ["ざじずぜぞ"],
        ["だぢづでど"],
        ["ばびぶべぼ"],
        ["ぱぴぷぺぽ"],
        ["ぁぃぅぇぉ"],
        ["っゃゅょ"],
        ["♂♀ー・："],
        ["ゔ"],
      ]
      
      return aiueoList.map(arr => arr.map(l => {
            return l.split('').map(t => {
            if (t == "　" || state.answeredLetter.has(t)) {
              return t;
            }
             return "■"
            })
            
      }))
    }

    function changeDefficulty(maxId, sedai) {
      state.pokemonData = null
      state.pokemonDataDetail = null
      state.input_answer = ''
      state.answer = ''
      state.answeredLetter = new Set()
      state.count = 0
      state.sedai = sedai
      getPokemon(maxId)

    }

    onMounted(() => {
      getPokemon(null)
    })
    return {state, getPokemon, getPlaceHolder, executeAnswer, clearCheck, getQuestion, getAnsweredTaiou, changeDefficulty}
  },
})
</script>

<style>
  .isMatch{
    color:red
  }
  .inline-list{
    display: inline;
  }
</style>

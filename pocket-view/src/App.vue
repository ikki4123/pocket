<template>
  <div>
    <div v-if="state.pokemonData != null">
      <img :src="state.pokemonData.sprites_front_default"/>
      <img :src="state.pokemonData.sprites_back_default"/>
      <p  v-if="state.pokemonData.stats != null">H: {{state.pokemonData["stats"]["h"]}}</p>
      <p  v-if="state.pokemonData.stats != null">A: {{state.pokemonData["stats"]["a"]}}</p>
      <p  v-if="state.pokemonData.stats != null">B: {{state.pokemonData["stats"]["b"]}}</p>
      <p  v-if="state.pokemonData.stats != null">C: {{state.pokemonData["stats"]["c"]}}</p>
      <p  v-if="state.pokemonData.stats != null">D: {{state.pokemonData["stats"]["d"]}}</p>
      <p  v-if="state.pokemonData.stats != null">S: {{state.pokemonData["stats"]["s"]}}</p>
    </div>
    <div v-if="state.pokemonDataDetail != null">
      <p  v-if="state.pokemonDataDetail.name != null">{{ state.pokemonDataDetail.name }}</p>
      <p  v-if="state.pokemonDataDetail.name != null">{{ state.pokemonDataDetail.name_hira }}</p>
      <p  v-if="state.pokemonDataDetail.name != null">{{ state.pokemonDataDetail.flavor_text_entry }}</p>
      <p  v-if="state.pokemonDataDetail.name != null">{{ state.pokemonDataDetail.flavor_text_entry_ja }}</p>
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
      response: null,
      pokemonData: null,
      pokemonDataDetail: null,
      imageUrl: null
    })

    async function getPokemon() {
      state.response = await axios.get('https://18j6btujfb.execute-api.ap-northeast-1.amazonaws.com/api/random')
      state.pokemonData = state.response.data
      state.imageUrl = state.pokemonData.sprites_back_default

      console.log(state.pokemonData)
      state.responseDetail = await axios.get('https://18j6btujfb.execute-api.ap-northeast-1.amazonaws.com/api/detail?id=' + state.pokemonData.id)
      state.pokemonDataDetail = state.responseDetail.data
    }
      
    onMounted(() => {
      getPokemon()
    })
    return {state, getPokemon}
  },
})
</script>

<style>
</style>

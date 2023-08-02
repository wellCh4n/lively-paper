<script setup>
import Question from "@/components/record/Question.vue"
import Answer from "@/components/record/Answer.vue";

defineProps({
  question: {
    type: String
  },
  answer: {
    type: String
  },
  answerCallback: {
    type: Function
  }
})
</script>

<template>
  <div style="display: flex; flex-direction: column; justify-content: center;">
    <Question :content="question" style="margin-top: 1rem" />
    <Answer :content="answer" :content-callback="answerCallback" style="margin-top: 1rem" />
  </div>
</template>

<style scoped>

</style>
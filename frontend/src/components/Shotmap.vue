<template>
	<v-container>
		<v-row align="center" justify="center">
			<h2>{{ title }}</h2>
		</v-row>
		<v-row align="center" justify="center">
			<img alt="Vue logo" src="../assets/rink2.png"/>
		</v-row>
	</v-container>
</template>
<script>
export default {
	props: {
		title: String
	},
	name: "Shotmap"
}
</script>
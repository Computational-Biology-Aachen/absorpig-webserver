<script lang="ts">
	import Spinner from '$lib/spinner/Spinner.svelte';

	import logo from '$lib/images/logo.png';
	const apiUrl = import.meta.env.BACKEND_URL;
	let result = $state(new Object());
	let img1 = $state('');
	let loading = $state(false);
	let postInit = $state(false);

	function readCsv(file: Blob) {
		return new Promise((resolve, reject) => {
			let content = '';
			const reader = new FileReader();

			reader.onloadend = (e: Event) => {
				const result = e.target.result;
				resolve(result);
			};
			reader.onerror = (e: any) => {
				reject(e);
			};
			reader.readAsText(file);
		});
	}

	async function onsubmit(event: Event) {
		event.preventDefault();

		loading = true;
		const formEl = event.target as HTMLFormElement;
		const data = new FormData(formEl);
		const file1 = data.get('absorption spectrum');
		const file2 = data.get('pigment spectrum');
		const chlConc: Number = data.get('chlorophyll concentration') ?? 1.0;
		const meanCellDiam: Number = data.get('mean cell diameter') ?? 1.0;
		const shiftSpectra: Boolean = data.get('shift spectra') ?? true;

		const fileContent1 = await readCsv(file1 as Blob);
		const fileContent2 = file2 ? await readCsv(file2 as Blob) : '';

		const url = 'http://127.0.0.1:8000';
		const response = await fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json;charset=utf-8'
			},
			body: JSON.stringify({
				absorption_spectrum: fileContent1,
				chl_concentration: chlConc,
				mean_diameter: meanCellDiam,
				pigment_spectrum: fileContent2,
				shift_spectra: shiftSpectra
			})
		});

		loading = false;
		postInit = true;
		const json = await response.json();
		result = json['pigment_composition'];

		const imgRaw = json['img'];
		img1 = `data:image/png;charset=utf-8;base64,${imgRaw}`;
	}

	// async function testServer(event: Event) {
	// 	const url = `http://127.0.0.1:8000/docs`;
	// 	console.log(url);
	// 	const response = await fetch(url);
	// 	console.log(response);
	// }
</script>

<div id="card">
	<div class="row">
		<div class="column">
			<h1>absorpig</h1>
			<p>
				Extract <b>pig</b>ment composition of measured <b>absor</b>ption spectra of photosynthetic
				organisms.
			</p>
		</div>
		<div class="column">
			<img src={logo} alt="absorpig logo" style="max-height: 150px; border-radius: 100%" />
		</div>
	</div>

	<!-- <form id="test" method="get" on:submit|preventDefault={testServer}>
		<input type="submit" />
	</form> -->

	<form id="file-upload" method="post" enctype="multipart/form-data" {onsubmit}>
		<label for="absorption spectrum"> Absorption spectrum</label>
		<input type="file" name="absorption spectrum" accept="text/csv" required />

		<label for="chlorophyll concentration"> Chlorophyll concentration</label>
		<input type="number" name="chlorophyll concentration" step="any" value="1.00" required />

		<label for="mean cell diameter"> Mean cell diameter</label>
		<input type="number" name="mean cell diameter" step="any" value="1.00" required />

		<label for="pigment spectrum"> Pigment spectrum (optional)</label>
		<input type="file" name="pigment spectrum" accept="text/csv" />

		<label for="shift spectra"> Shift spectra</label>
		<input type="checkbox" name="shift spectra" required checked />

		<input type="submit" style="grid-column: span 2;" />
	</form>

	<div id="results">
		{#if loading}
			<Spinner></Spinner>
		{:else if postInit}
			<h2>Results</h2>
			<img src={img1} alt="pigment composition" />
			<h3>Pigment composition</h3>
			<div id="pigment-composition">
				{#each Object.entries(result) as [pigment, value]}
					<pre>{pigment}</pre>
					<pre>{value.toFixed(4)}</pre>
				{/each}
			</div>
		{/if}
	</div>

	<div>
		<h2>Data format</h2>
		<h3>Absorption spectrum</h3>
		<p>
			The absorption spectrum is expected to be in a <code>.csv</code> format. The index is assumed to
			represent the wavelength in nanometers and the first column to be the absorption.
		</p>
		<p>Example file:</p>
		<pre>
wavelength_nm,absorption
396,0.0211
397,0.0216
398,0.022
399,0.0224
        </pre>

		<h3>Pigment spectrum</h3>
		<p>
			The pigment spectrum is expected to be in a <code>.csv</code> format. The index is assumed to represent
			the wavelength in nanometers, and each column to be the absorption per pigment.
		</p>
		<p>Example file:</p>
		<pre>
wavelength_nm,Chla,PC,APC
396,0.0169,0.0002,0.0002
397,0.0171,0.0002,0.0002
398,0.0174,0.0002,0.0002
399,0.0176,0.0002,0.0002
400,0.0178,0.0002,0.0002
        </pre>
	</div>
</div>

<style>
	#card {
		background: #121212;
		padding: 2rem 3rem;
		margin: 2rem;
		max-width: 600px;
		display: flex;
		flex-direction: column;
		justify-content: center;
		gap: 3rem;
		box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
	}

	#file-upload {
		width: 100%;
		display: grid;
		grid-template-columns: max-content max-content;
		grid-gap: 5px;
		justify-content: center;
	}

	#pigment-composition {
		width: 100%;
		display: grid;
		grid-template-columns: max-content max-content;
		grid-gap: 0 5px;
		justify-content: left;
	}

	input[type='submit'] {
		background-color: var(--header-color);
		border: none;
		border-radius: 5px;
		color: white;
		padding: 5px 0;
		cursor: pointer;
	}

	input[type='submit']:hover {
		filter: brightness(85%);
	}

	input[type='file']::file-selector-button {
		background-color: var(--header-color);
		border: none;
		border-radius: 5px;
		color: white;
		cursor: pointer;
	}

	input[type='file']::file-selector-button:hover {
		filter: brightness(85%);
	}
	.row {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 20px;
	}

	img {
		max-width: 100%;
	}
</style>

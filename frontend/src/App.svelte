<script>
  import FileUploader from './lib/FileUploader.svelte';

  let geojson = null;
  let boundaryColumns = [];
  let electionColumns = [];

  function handleUploaded(event) {
    ({ geojson, boundaryColumns, electionColumns } = event.detail);
  }
</script>

<main>
  <h1>Redistricting Precinct Cleaner</h1>

  <FileUploader on:uploaded={handleUploaded} />

  {#if geojson}
    <section class="results">
      <h2>Upload successful</h2>
      <p><strong>Boundary columns:</strong> {boundaryColumns.join(', ')}</p>
      <p><strong>Election columns:</strong> {electionColumns.join(', ')}</p>
    </section>
  {/if}
</main>

<style>
  main {
    max-width: 800px;
    margin: 2rem auto;
    font-family: sans-serif;
    padding: 0 1rem;
  }
</style>

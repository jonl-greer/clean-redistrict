<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let boundaryFile = null;
  let electionFile = null;
  let loading = false;
  let error = null;

  function handleDrop(field, event) {
    event.preventDefault();
    const file = event.dataTransfer?.files[0] ?? event.target.files[0];
    if (!file) return;
    if (field === 'boundary') boundaryFile = file;
    else electionFile = file;
  }

  function handleInput(field, event) {
    const file = event.target.files[0];
    if (!file) return;
    if (field === 'boundary') boundaryFile = file;
    else electionFile = file;
  }

  async function upload() {
    if (!boundaryFile || !electionFile) return;
    loading = true;
    error = null;

    const form = new FormData();
    form.append('boundary', boundaryFile);
    form.append('election', electionFile);

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: form,
      });

      if (!res.ok) {
        const detail = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(detail.detail ?? res.statusText);
      }

      const data = await res.json();
      dispatch('uploaded', {
        geojson: data.boundary.geojson,
        boundaryColumns: data.boundary.columns,
        electionColumns: data.election.columns,
      });
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }
</script>

<div class="uploader">
  <div class="zones">
    <label
      class="zone"
      class:filled={boundaryFile}
      on:dragover|preventDefault
      on:drop={(e) => handleDrop('boundary', e)}
    >
      <input type="file" accept=".zip" on:change={(e) => handleInput('boundary', e)} hidden />
      <span class="label">Boundary shapefile (.zip)</span>
      <span class="filename">{boundaryFile ? boundaryFile.name : 'Click or drag to upload'}</span>
    </label>

    <label
      class="zone"
      class:filled={electionFile}
      on:dragover|preventDefault
      on:drop={(e) => handleDrop('election', e)}
    >
      <input type="file" accept=".zip" on:change={(e) => handleInput('election', e)} hidden />
      <span class="label">Election results (.zip)</span>
      <span class="filename">{electionFile ? electionFile.name : 'Click or drag to upload'}</span>
    </label>
  </div>

  {#if error}
    <p class="error">{error}</p>
  {/if}

  <button on:click={upload} disabled={!boundaryFile || !electionFile || loading}>
    {loading ? 'Processing…' : 'Upload & Clean'}
  </button>
</div>

<style>
  .uploader {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .zones {
    display: flex;
    gap: 1rem;
  }

  .zone {
    flex: 1;
    border: 2px dashed #aaa;
    border-radius: 8px;
    padding: 2rem 1rem;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    transition: border-color 0.2s;
  }

  .zone:hover {
    border-color: #555;
  }

  .zone.filled {
    border-color: #2a7a2a;
    background: #f0fff0;
  }

  .label {
    font-weight: 600;
    font-size: 0.9rem;
  }

  .filename {
    font-size: 0.8rem;
    color: #555;
    word-break: break-all;
    text-align: center;
  }

  button {
    align-self: flex-start;
    padding: 0.5rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .error {
    color: #c00;
    font-size: 0.9rem;
  }
</style>

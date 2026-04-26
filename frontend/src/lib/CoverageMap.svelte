<script>
  import us from 'us-atlas/states-10m.json';
  import { feature as topojsonFeature } from 'topojson-client';
  import { geoAlbersUsa, geoPath } from 'd3-geo';

  export let coverageData = [];

  const mapWidth = 975;
  const mapHeight = 610;
  const histWidth = 290;
  const histHeight = 170;
  const histMargin = { top: 18, right: 10, bottom: 40, left: 30 };
  const missingFill = '#e5e7eb';

  const stateFeatures = topojsonFeature(us, us.objects.states).features;

  const stateNameById = {
    '01': 'Alabama',
    '02': 'Alaska',
    '04': 'Arizona',
    '05': 'Arkansas',
    '06': 'California',
    '08': 'Colorado',
    '09': 'Connecticut',
    '10': 'Delaware',
    '11': 'District of Columbia',
    '12': 'Florida',
    '13': 'Georgia',
    '15': 'Hawaii',
    '16': 'Idaho',
    '17': 'Illinois',
    '18': 'Indiana',
    '19': 'Iowa',
    '20': 'Kansas',
    '21': 'Kentucky',
    '22': 'Louisiana',
    '23': 'Maine',
    '24': 'Maryland',
    '25': 'Massachusetts',
    '26': 'Michigan',
    '27': 'Minnesota',
    '28': 'Mississippi',
    '29': 'Missouri',
    '30': 'Montana',
    '31': 'Nebraska',
    '32': 'Nevada',
    '33': 'New Hampshire',
    '34': 'New Jersey',
    '35': 'New Mexico',
    '36': 'New York',
    '37': 'North Carolina',
    '38': 'North Dakota',
    '39': 'Ohio',
    '40': 'Oklahoma',
    '41': 'Oregon',
    '42': 'Pennsylvania',
    '44': 'Rhode Island',
    '45': 'South Carolina',
    '46': 'South Dakota',
    '47': 'Tennessee',
    '48': 'Texas',
    '49': 'Utah',
    '50': 'Vermont',
    '51': 'Virginia',
    '53': 'Washington',
    '54': 'West Virginia',
    '55': 'Wisconsin',
    '56': 'Wyoming'
  };

  const abbr = {
    Alabama: 'AL',
    Alaska: 'AK',
    Arizona: 'AZ',
    Arkansas: 'AR',
    California: 'CA',
    Colorado: 'CO',
    Connecticut: 'CT',
    Delaware: 'DE',
    'District of Columbia': 'DC',
    Florida: 'FL',
    Georgia: 'GA',
    Hawaii: 'HI',
    Idaho: 'ID',
    Illinois: 'IL',
    Indiana: 'IN',
    Iowa: 'IA',
    Kansas: 'KS',
    Kentucky: 'KY',
    Louisiana: 'LA',
    Maine: 'ME',
    Maryland: 'MD',
    Massachusetts: 'MA',
    Michigan: 'MI',
    Minnesota: 'MN',
    Mississippi: 'MS',
    Missouri: 'MO',
    Montana: 'MT',
    Nebraska: 'NE',
    Nevada: 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    Ohio: 'OH',
    Oklahoma: 'OK',
    Oregon: 'OR',
    Pennsylvania: 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    Tennessee: 'TN',
    Texas: 'TX',
    Utah: 'UT',
    Vermont: 'VT',
    Virginia: 'VA',
    Washington: 'WA',
    'West Virginia': 'WV',
    Wisconsin: 'WI',
    Wyoming: 'WY'
  };

  const tiles = [
    ['Maine', 10, 1],
    ['Washington', 1, 2],
    ['Montana', 2, 2],
    ['North Dakota', 3, 2],
    ['Minnesota', 4, 2],
    ['Wisconsin', 5, 2],
    ['Michigan', 6, 2],
    ['New York', 8, 2],
    ['Vermont', 9, 2],
    ['New Hampshire', 10, 2],
    ['Massachusetts', 11, 2],
    ['Oregon', 1, 3],
    ['Idaho', 2, 3],
    ['South Dakota', 3, 3],
    ['Iowa', 4, 3],
    ['Illinois', 5, 3],
    ['Indiana', 6, 3],
    ['Ohio', 7, 3],
    ['Pennsylvania', 8, 3],
    ['New Jersey', 9, 3],
    ['Connecticut', 10, 3],
    ['Rhode Island', 11, 3],
    ['California', 1, 4],
    ['Nevada', 2, 4],
    ['Wyoming', 3, 4],
    ['Nebraska', 4, 4],
    ['Missouri', 5, 4],
    ['Kentucky', 6, 4],
    ['West Virginia', 7, 4],
    ['Virginia', 8, 4],
    ['Maryland', 9, 4],
    ['Delaware', 10, 4],
    ['Arizona', 2, 5],
    ['Utah', 3, 5],
    ['Colorado', 4, 5],
    ['Kansas', 5, 5],
    ['Arkansas', 6, 5],
    ['Tennessee', 7, 5],
    ['North Carolina', 8, 5],
    ['South Carolina', 9, 5],
    ['Alaska', 1, 6],
    ['New Mexico', 3, 6],
    ['Oklahoma', 4, 6],
    ['Louisiana', 5, 6],
    ['Mississippi', 6, 6],
    ['Alabama', 7, 6],
    ['Georgia', 8, 6],
    ['Hawaii', 1, 7],
    ['Texas', 4, 7],
    ['Florida', 9, 7]
  ];

  const tileLookup = Object.fromEntries(
    tiles.map(([state, col, row]) => [state, { col, row }])
  );

  const stateCallouts = {
    Vermont: { x: 835, y: 88 },
    'New Hampshire': { x: 900, y: 110 },
    Massachusetts: { x: 928, y: 150 },
    'Rhode Island': { x: 932, y: 174 },
    Connecticut: { x: 920, y: 204 },
    'New Jersey': { x: 888, y: 245 },
    Delaware: { x: 888, y: 273 },
    Maryland: { x: 875, y: 302 },
    'District of Columbia': { x: 900, y: 326 }
  };

  let mapType = 'geographic';
  let colorBy = 'score';
  let selectedName = '';
  let hovered = null;

  let tooltip = {
    show: false,
    x: 0,
    y: 0
  };

  $: rows = prepareData(coverageData);
  $: scored = scoreRows(rows);
  $: dataByState = Object.fromEntries(scored.map((d) => [d.state, d]));
  $: maxSources = Math.max(1, ...scored.map((d) => d.numSources));
  $: maxYears = Math.max(1, ...scored.map((d) => d.numYears));

  $: if (!selectedName && scored.length) {
    selectedName = scored[0].state;
  }

  $: if (selectedName && !scored.find((d) => d.state === selectedName) && scored.length) {
    selectedName = scored[0].state;
  }

  $: selected = scored.find((d) => d.state === selectedName) || scored[0];

  $: mappedTiles = scored
    .map((d) => ({ ...d, ...tileLookup[d.state] }))
    .filter((d) => d.col)
    .map((d) => ({
      ...d,
      fill: getFill(d, colorBy, maxSources, maxYears),
      textColor: getTextColor(d, colorBy, maxSources, maxYears)
    }));

  $: projection = geoAlbersUsa().fitSize(
    [mapWidth, mapHeight],
    {
      type: 'FeatureCollection',
      features: stateFeatures
    }
  );

  $: pathGenerator = geoPath(projection);

  $: geographicStates = stateFeatures
    .map((shape) => {
      const stateName = getStateName(shape);
      const data = dataByState[stateName];

      return {
        name: stateName,
        shape,
        data,
        path: pathGenerator(shape),
        fill: data ? getFill(data, colorBy, maxSources, maxYears) : missingFill
      };
    })
    .filter((d) => d.path && d.name !== 'District of Columbia');

  $: geographicLabels = geographicStates
    .map((state) => {
      const centroid = pathGenerator.centroid(state.shape);
      const callout = stateCallouts[state.name];

      if (!centroid || centroid.some((value) => !Number.isFinite(value))) {
        return null;
      }

      return {
        name: state.name,
        abbr: abbr[state.name] || state.name.slice(0, 2).toUpperCase(),
        data: state.data,
        x: callout ? callout.x : centroid[0],
        y: callout ? callout.y : centroid[1],
        lineX: centroid[0],
        lineY: centroid[1],
        bendX: callout ? callout.x - 18 : null,
        callout: Boolean(callout),
        textColor: state.data
          ? getTextColor(state.data, colorBy, maxSources, maxYears)
          : '#0f172a',
        textStroke: state.data
          ? getTextStroke(state.data, colorBy, maxSources, maxYears)
          : 'white'
      };
    })
    .filter(Boolean);

  $: legend = getLegend(colorBy, maxSources, maxYears);
  $: summaryMetric = getSummaryMetric(colorBy, scored);
  $: histogram = buildHistogram(colorBy, scored, selected);
  $: histogramLayout = layoutHistogram(histogram);

  function getStateName(shape) {
    if (shape.properties?.name) {
      return shape.properties.name;
    }

    const id = String(shape.id).padStart(2, '0');
    return stateNameById[id] || String(shape.id);
  }

  function prepareData(data) {
    return (data || [])
      .filter((d) => d?.state && typeof d.has_statewide_shp === 'boolean')
      .map((d) => {
        const years = [...new Set((d.years_covered || []).map(Number).filter(Number.isFinite))]
          .sort((a, b) => a - b);

        const sources = [...new Set((d.data_sources || []).map(cleanSource).filter(Boolean))];

        return {
          ...d,
          years_covered: years,
          data_sources: sources,
          data_format: Array.isArray(d.data_format) ? d.data_format : [],
          abbr: abbr[d.state] || d.state.slice(0, 2).toUpperCase(),
          numYears: years.length,
          numSources: sources.length,
          earliest: years.length ? Math.min(...years) : null,
          latest: years.length ? Math.max(...years) : null,
          has2024: years.includes(2024),
          hasHistorical: years.some((y) => y <= 2014)
        };
      });
  }

  function cleanSource(source) {
    const s = String(source).trim();

    if (!s) return '';
    if (s.toUpperCase().includes('MGGG')) return 'MGGG';
    if (s.toLowerCase() === 'other') return 'other';
    if (s.toLowerCase() === 'state') return 'State';

    return s.toUpperCase();
  }

  function featureVector(d) {
    const sources = new Set(d.data_sources);

    return [
      d.likely_joinable ? 1 : 0,
      d.numSources,
      d.numYears,
      d.earliest ? 2026 - d.earliest : 0,
      d.hasHistorical ? 1 : 0,
      d.has2024 ? 1 : 0,
      sources.has('RDH') ? 1 : 0,
      sources.has('VEST') ? 1 : 0,
      sources.has('MGGG') ? 1 : 0,
      sources.has('PGP') ? 1 : 0,
      sources.has('other') ? 1 : 0
    ];
  }

  function scoreRows(data) {
    if (!data.length) return [];

    const weights = [4, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1];
    const X = data.map(featureVector);

    const means = weights.map((_, j) => avg(X.map((row) => row[j])));
    const sds = weights.map((_, j) => sd(X.map((row) => row[j])) || 1);

    const raw = X.map((row) =>
      row.reduce((sum, value, j) => {
        return sum + ((value - means[j]) / sds[j]) * weights[j];
      }, 0)
    );

    const min = Math.min(...raw);
    const max = Math.max(...raw);
    const range = max - min || 1;

    return data.map((d, i) => {
      const score100 = Math.round(((raw[i] - min) / range) * 100);

      return {
        ...d,
        rawScore: raw[i],
        score100
      };
    });
  }

  function avg(values) {
    return values.length
      ? values.reduce((sum, value) => sum + value, 0) / values.length
      : 0;
  }

  function sd(values) {
    if (!values.length) return 0;
    const m = avg(values);
    return Math.sqrt(avg(values.map((value) => (value - m) ** 2)));
  }

  function getSummaryMetric(mode, data) {
    if (!data.length) {
      return {
        label: 'No data',
        value: '—',
        note: ''
      };
    }

    if (mode === 'sources') {
      return {
        label: 'Average number of sources',
        value: avg(data.map((d) => d.numSources)).toFixed(1),
        note: 'Average distinct data sources per state.'
      };
    }

    if (mode === 'years') {
      return {
        label: 'Average years covered',
        value: avg(data.map((d) => d.numYears)).toFixed(1),
        note: 'Average number of election years covered per state.'
      };
    }

    if (mode === 'recent') {
      const count = data.filter((d) => d.has2024).length;
      return {
        label: 'States with 2024 data',
        value: String(count),
        note: `${count} of ${data.length} states include 2024.`
      };
    }

    return {
      label: 'Average composite score',
      value: avg(data.map((d) => d.score100)).toFixed(1),
      note: 'Average score on the 0–100 coverage scale.'
    };
  }

  function sequentialBlue(value, maxValue = 100) {
    const t = Math.max(0, Math.min(1, maxValue ? value / maxValue : 0));
    const lightness = 94 - t * 52;
    return `hsl(217, 76%, ${lightness}%)`;
  }

  function getFill(d, mode, maxSourcesValue, maxYearsValue) {
    if (mode === 'sources') {
      return sequentialBlue(d.numSources, maxSourcesValue);
    }

    if (mode === 'years') {
      return sequentialBlue(d.numYears, maxYearsValue);
    }

    if (mode === 'recent') {
      return d.has2024 ? sequentialBlue(100, 100) : sequentialBlue(25, 100);
    }

    return sequentialBlue(d.score100, 100);
  }

  function getIntensity(d, mode, maxSourcesValue, maxYearsValue) {
    if (mode === 'sources') {
      return maxSourcesValue ? d.numSources / maxSourcesValue : 0;
    }

    if (mode === 'years') {
      return maxYearsValue ? d.numYears / maxYearsValue : 0;
    }

    if (mode === 'recent') {
      return d.has2024 ? 1 : 0.25;
    }

    return d.score100 / 100;
  }

  function getTextColor(d, mode, maxSourcesValue, maxYearsValue) {
    return getIntensity(d, mode, maxSourcesValue, maxYearsValue) > 0.58
      ? 'white'
      : '#0f172a';
  }

  function getTextStroke(d, mode, maxSourcesValue, maxYearsValue) {
    return getIntensity(d, mode, maxSourcesValue, maxYearsValue) > 0.58
      ? '#0f172a'
      : 'white';
  }

  function getLegend(mode, maxSourcesValue, maxYearsValue) {
    if (mode === 'sources') {
      return {
        type: 'gradient',
        title: 'Number of data sources',
        low: 'Fewer',
        high: `${maxSourcesValue} source${maxSourcesValue === 1 ? '' : 's'}`
      };
    }

    if (mode === 'years') {
      return {
        type: 'gradient',
        title: 'Years covered',
        low: 'Fewer',
        high: `${maxYearsValue} year${maxYearsValue === 1 ? '' : 's'}`
      };
    }

    if (mode === 'recent') {
      return {
        type: 'categories',
        title: 'Includes 2024 data',
        items: [
          ['No', sequentialBlue(25, 100)],
          ['Yes', sequentialBlue(100, 100)]
        ]
      };
    }

    return {
      type: 'gradient',
      title: 'Coverage score',
      low: '0',
      high: '100'
    };
  }

  function showTip(event, item) {
    hovered = item;

    const x = event.clientX || window.innerWidth / 2;
    const y = event.clientY || window.innerHeight / 2;

    tooltip = {
      show: true,
      x: x + 14,
      y: y + 14
    };
  }

  function hideTip() {
    tooltip = {
      show: false,
      x: 0,
      y: 0
    };
  }

  function selectState(data) {
    if (data) {
      selectedName = data.state;
    }
  }

  function handleStateKeydown(event, data) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      selectState(data);
    }
  }

  function yearCountText(d) {
    if (!d?.numYears) return 'No years listed';
    return `${d.numYears} year${d.numYears === 1 ? '' : 's'} covered`;
  }

  function yearListText(d) {
    return d?.years_covered?.length ? d.years_covered.join(', ') : 'None listed';
  }

  function listText(values) {
    return values?.length ? values.join(', ') : 'None listed';
  }

  function buildHistogram(mode, data, selectedState) {
    if (!data.length) {
      return {
        title: '',
        selectedDisplay: '',
        bars: []
      };
    }

    if (mode === 'years') {
      const max = Math.max(1, ...data.map((d) => d.numYears));
      const bars = Array.from({ length: max + 1 }, (_, i) => ({
        key: i,
        label: String(i),
        count: 0,
        isSelected: false
      }));

      data.forEach((d) => {
        bars[d.numYears].count += 1;
      });

      if (selectedState) {
        bars[selectedState.numYears].isSelected = true;
      }

      return {
        title: 'Years covered',
        selectedDisplay: selectedState
          ? `${selectedState.state}: ${selectedState.numYears} year${selectedState.numYears === 1 ? '' : 's'}`
          : '',
        bars
      };
    }

    if (mode === 'sources') {
      const max = Math.max(1, ...data.map((d) => d.numSources));
      const bars = Array.from({ length: max + 1 }, (_, i) => ({
        key: i,
        label: String(i),
        count: 0,
        isSelected: false
      }));

      data.forEach((d) => {
        bars[d.numSources].count += 1;
      });

      if (selectedState) {
        bars[selectedState.numSources].isSelected = true;
      }

      return {
        title: 'Data sources',
        selectedDisplay: selectedState
          ? `${selectedState.state}: ${selectedState.numSources} source${selectedState.numSources === 1 ? '' : 's'}`
          : '',
        bars
      };
    }

    if (mode === 'recent') {
      const bars = [
        { key: 0, label: 'No', count: 0, isSelected: false },
        { key: 1, label: 'Yes', count: 0, isSelected: false }
      ];

      data.forEach((d) => {
        bars[d.has2024 ? 1 : 0].count += 1;
      });

      if (selectedState) {
        bars[selectedState.has2024 ? 1 : 0].isSelected = true;
      }

      return {
        title: '2024 data',
        selectedDisplay: selectedState
          ? `${selectedState.state}: ${selectedState.has2024 ? 'Includes 2024' : 'No 2024 listed'}`
          : '',
        bars
      };
    }

    const bins = Array.from({ length: 10 }, (_, i) => ({
      key: i,
      label: i === 9 ? '90-100' : `${i * 10}-${i * 10 + 9}`,
      count: 0,
      isSelected: false
    }));

    data.forEach((d) => {
      const idx = d.score100 === 100 ? 9 : Math.floor(d.score100 / 10);
      bins[idx].count += 1;
    });

    if (selectedState) {
      const idx = selectedState.score100 === 100 ? 9 : Math.floor(selectedState.score100 / 10);
      bins[idx].isSelected = true;
    }

    return {
      title: 'Composite score',
      selectedDisplay: selectedState
        ? `${selectedState.state}: ${selectedState.score100}/100`
        : '',
      bars: bins
    };
  }

  function layoutHistogram(histogramData) {
    const innerWidth = histWidth - histMargin.left - histMargin.right;
    const innerHeight = histHeight - histMargin.top - histMargin.bottom;
    const barCount = Math.max(1, histogramData.bars.length);
    const gap = Math.min(6, innerWidth / (barCount * 4));
    const barWidth = (innerWidth - gap * (barCount - 1)) / barCount;
    const maxCount = Math.max(1, ...histogramData.bars.map((bar) => bar.count));

    const bars = histogramData.bars.map((bar, index) => {
      const height = (bar.count / maxCount) * innerHeight;
      const x = histMargin.left + index * (barWidth + gap);
      const y = histMargin.top + innerHeight - height;

      return {
        ...bar,
        x,
        y,
        width: barWidth,
        height,
        labelX: x + barWidth / 2
      };
    });

    const ticks = [...new Set([0, maxCount])]
      .sort((a, b) => a - b)
      .map((value) => ({
        value,
        y: histMargin.top + innerHeight - (value / maxCount) * innerHeight
      }));

    return {
      width: histWidth,
      height: histHeight,
      maxCount,
      bars,
      ticks
    };
  }
</script>

<section class="coverage-card" aria-labelledby="coverage-heading">
  <div class="header-row">
    <div class="title-block">
      <p class="eyebrow">Coverage map</p>
      <h2 id="coverage-heading">Precinct data quality and availability by state</h2>
      <p class="subhead">
        Hover over a state for a quick summary. Click a state for details and to highlight its bin.
      </p>
    </div>

    <div class="controls">
      <label>
        <span>Map type</span>
        <select bind:value={mapType}>
          <option value="geographic">Geographic map</option>
          <option value="tiles">Tile map</option>
        </select>
      </label>

      <label>
        <span>Color by</span>
        <select bind:value={colorBy}>
          <option value="score">Composite score</option>
          <option value="sources">Number of sources</option>
          <option value="years">Years covered</option>
          <option value="recent">Includes 2024 data</option>
        </select>
      </label>
    </div>
  </div>

  {#if !scored.length}
    <div class="empty-state">
      <strong>No coverage data loaded yet.</strong>
      <p>
        Make sure <code>coverage.json</code> is inside <code>frontend/public/coverage.json</code>.
      </p>
    </div>
  {:else}
    <div class="content-grid">
      <div class="map-card">
        <div class="map-summary-bar">
          <div class="map-summary-chip">
            <p class="eyebrow">Summary</p>
            <strong>{summaryMetric.value}</strong>
            <span>{summaryMetric.label}</span>
            <small>{summaryMetric.note}</small>
          </div>
        </div>

        {#if mapType === 'geographic'}
          <svg
            class="geo-map"
            viewBox={`0 0 ${mapWidth} ${mapHeight}`}
            role="img"
            aria-label="Geographic map of state precinct data coverage"
          >
            {#each geographicStates as state}
              <path
                d={state.path}
                class:selected={selected?.state === state.name}
                class:missing={!state.data}
                class="geo-state"
                fill={state.fill}
                role={state.data ? 'button' : 'img'}
                tabindex={state.data ? 0 : -1}
                aria-label={state.data ? `${state.name}: score ${state.data.score100}` : `${state.name}: no coverage data`}
                on:mouseenter={(event) => showTip(event, state)}
                on:mousemove={(event) => showTip(event, state)}
                on:mouseleave={hideTip}
                on:focus={(event) => showTip(event, state)}
                on:blur={hideTip}
                on:keydown={(event) => handleStateKeydown(event, state.data)}
                on:click={() => selectState(state.data)}
              />
            {/each}

            {#each geographicLabels.filter((label) => label.callout) as label}
              <polyline
                class="state-callout-line"
                points={`${label.lineX},${label.lineY} ${label.bendX},${label.y} ${label.x - 6},${label.y}`}
              />

              <text
                class="state-label callout-label"
                x={label.x}
                y={label.y}
                text-anchor="start"
                dominant-baseline="middle"
              >
                {label.abbr}
              </text>
            {/each}

            {#each geographicLabels.filter((label) => !label.callout) as label}
              <text
                class="state-label"
                x={label.x}
                y={label.y}
                text-anchor="middle"
                dominant-baseline="middle"
                style={`fill: ${label.textColor}; --label-stroke: ${label.textStroke};`}
              >
                {label.abbr}
              </text>
            {/each}
          </svg>
        {:else}
          <div class="tile-map" role="img" aria-label="Tile map of state precinct data coverage">
            {#each mappedTiles as d}
              <button
                type="button"
                class:selected={selected?.state === d.state}
                class="state-tile"
                style={`grid-column: ${d.col}; grid-row: ${d.row}; background: ${d.fill}; color: ${d.textColor};`}
                aria-label={`${d.state}: score ${d.score100}`}
                on:mouseenter={(event) => showTip(event, { data: d, name: d.state })}
                on:mousemove={(event) => showTip(event, { data: d, name: d.state })}
                on:mouseleave={hideTip}
                on:focus={(event) => showTip(event, { data: d, name: d.state })}
                on:blur={hideTip}
                on:click={() => selectState(d)}
              >
                {d.abbr}
              </button>
            {/each}
          </div>
        {/if}

        <div class="legend">
          <strong>{legend.title}:</strong>

          {#if legend.type === 'gradient'}
            <div class="gradient-legend">
              <span>{legend.low}</span>
              <i></i>
              <span>{legend.high}</span>
            </div>
          {:else}
            <div class="category-legend">
              {#each legend.items as [label, color]}
                <span>
                  <i style={`background: ${color};`}></i>
                  {label}
                </span>
              {/each}
            </div>
          {/if}

          <span class="missing-key">
            <i></i>
            No data in coverage.json
          </span>
        </div>
      </div>

      <aside class="right-column">
        {#if selected}
          <section class="detail-panel">
            <p class="eyebrow">Selected state</p>
            <h3>{selected.state}</h3>

            <dl>
              <div>
                <dt>Years covered</dt>
                <dd>{yearListText(selected)}</dd>
              </div>

              <div>
                <dt>Data sources</dt>
                <dd>{listText(selected.data_sources)}</dd>
              </div>

              <div>
                <dt>Data format</dt>
                <dd>{listText(selected.data_format)}</dd>
              </div>
            </dl>
          </section>
        {/if}

        <section class="histogram-card">
          <div class="histogram-header">
            <p class="eyebrow">Histogram</p>
            <h3>{histogram.title}</h3>
            {#if selected}
              <p>{histogram.selectedDisplay}</p>
            {/if}
          </div>

          <svg
            class="histogram-svg"
            viewBox={`0 0 ${histogramLayout.width} ${histogramLayout.height}`}
            role="img"
            aria-label={histogram.title}
          >
            {#each histogramLayout.ticks as tick}
              <line
                x1={histMargin.left}
                x2={histWidth - histMargin.right}
                y1={tick.y}
                y2={tick.y}
                class="hist-grid"
              />
              <text
                x={histMargin.left - 6}
                y={tick.y}
                text-anchor="end"
                dominant-baseline="middle"
                class="hist-tick-label"
              >
                {tick.value}
              </text>
            {/each}

            <line
              x1={histMargin.left}
              x2={histMargin.left}
              y1={histMargin.top}
              y2={histHeight - histMargin.bottom}
              class="hist-axis"
            />
            <line
              x1={histMargin.left}
              x2={histWidth - histMargin.right}
              y1={histHeight - histMargin.bottom}
              y2={histHeight - histMargin.bottom}
              class="hist-axis"
            />

            {#each histogramLayout.bars as bar}
              <rect
                x={bar.x}
                y={bar.y}
                width={bar.width}
                height={bar.height}
                rx="4"
                class:selected-bar={bar.isSelected}
                class="hist-bar"
              />

              <text
                x={bar.labelX}
                y={histHeight - histMargin.bottom + 14}
                text-anchor="middle"
                class="hist-x-label"
              >
                {bar.label}
              </text>

              {#if bar.count > 0}
                <text
                  x={bar.labelX}
                  y={bar.y - 5}
                  text-anchor="middle"
                  class:selected-count={bar.isSelected}
                  class="hist-count"
                >
                  {bar.count}
                </text>
              {/if}
            {/each}
          </svg>
        </section>
      </aside>
    </div>
  {/if}

  {#if tooltip.show && hovered}
    <div class="tooltip" style={`left: ${tooltip.x}px; top: ${tooltip.y}px;`}>
      {#if hovered.data}
        <strong>{hovered.data.state}</strong>
        <span>Score: {hovered.data.score100}/100</span>
        <span>Sources: {listText(hovered.data.data_sources)}</span>
        <span>Years: {yearCountText(hovered.data)}</span>
      {:else}
        <strong>{hovered.name}</strong>
        <span>No coverage data loaded for this state.</span>
      {/if}
    </div>
  {/if}
</section>

<style>
  .coverage-card {
    position: relative;
    width: min(95vw, 1380px);
    margin: 0 auto;
    padding: 1rem 1.1rem;
    border: 1px solid #e2e8f0;
    border-radius: 24px;
    background: white;
    box-shadow: 0 18px 45px rgba(25, 35, 60, 0.08);
  }

  .header-row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.8rem;
    align-items: start;
  }

  .title-block {
    flex: 1 1 auto;
    min-width: 0;
  }

  .eyebrow {
    margin: 0 0 0.35rem;
    color: #64748b;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  h2,
  h3,
  p {
    margin-top: 0;
  }

  h2 {
    margin-bottom: 0.25rem;
    font-size: clamp(1.7rem, 2.8vw, 2.8rem);
    line-height: 1.08;
    color: #172033;
    max-width: 760px;
  }

  h3 {
    margin-bottom: 0.35rem;
    color: #172033;
    font-size: 1.2rem;
  }

  .subhead {
    max-width: 720px;
    margin-bottom: 0;
    color: #536173;
    line-height: 1.4;
    font-size: 1rem;
  }

  .controls {
    display: flex;
    gap: 0.75rem;
    align-items: end;
    flex-wrap: wrap;
    flex: 0 0 auto;
  }

  label {
    display: grid;
    gap: 0.35rem;
    min-width: 175px;
    color: #536173;
    font-weight: 700;
  }

  select {
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    background: #f8fafc;
    color: #172033;
    font: inherit;
    padding: 0.62rem 0.72rem;
  }

  .empty-state {
    padding: 1rem;
    border: 1px dashed #cbd5e1;
    border-radius: 16px;
    background: #f8fafc;
    color: #475569;
  }

  .empty-state p {
    margin-bottom: 0;
  }

  .content-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.42fr) 320px;
    gap: 0.9rem;
    align-items: start;
  }

  .right-column {
    display: grid;
    gap: 0.8rem;
  }

  .map-card,
  .detail-panel,
  .histogram-card {
    padding: 0.85rem;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    background: #fbfdff;
  }

  .map-summary-bar {
    margin-bottom: 0.55rem;
  }

  .map-summary-chip {
    max-width: 360px;
    margin: 0 auto;
    padding: 0.7rem 0.9rem;
    border: 1px solid #dbeafe;
    border-radius: 16px;
    background: linear-gradient(180deg, #f8fbff 0%, #eff6ff 100%);
    text-align: center;
  }

  .map-summary-chip strong {
    display: block;
    color: #1d4ed8;
    font-size: 1.9rem;
    line-height: 1;
    margin-bottom: 0.2rem;
  }

  .map-summary-chip span {
    display: block;
    color: #1e293b;
    font-weight: 800;
    line-height: 1.2;
  }

  .map-summary-chip small {
    display: block;
    color: #64748b;
    margin-top: 0.18rem;
    line-height: 1.3;
  }

  .geo-map {
    display: block;
    width: 100%;
    min-width: 690px;
    height: auto;
  }

  .geo-state {
    stroke: white;
    stroke-width: 1.2;
    cursor: pointer;
    transition:
      fill 0.22s ease,
      stroke 0.18s ease,
      stroke-width 0.18s ease,
      opacity 0.18s ease;
  }

  .geo-state:hover,
  .geo-state:focus,
  .geo-state.selected {
    stroke: #0f172a;
    stroke-width: 2.5;
    outline: none;
  }

  .geo-state.missing {
    cursor: default;
    opacity: 0.85;
  }

  .state-label {
    pointer-events: none;
    font-size: 17px;
    font-weight: 800;
    fill: #0f172a;
    paint-order: stroke;
    stroke: var(--label-stroke, white);
    stroke-width: 3px;
    stroke-linejoin: round;
  }

  .callout-label {
    fill: #0f172a;
    stroke: white;
  }

  .state-callout-line {
    fill: none;
    pointer-events: none;
    stroke: #475569;
    stroke-width: 1.4;
    stroke-linecap: round;
    stroke-linejoin: round;
    opacity: 0.95;
  }

  .tile-map {
    display: grid;
    grid-template-columns: repeat(11, 48px);
    grid-template-rows: repeat(7, 40px);
    gap: 7px;
    min-width: 598px;
  }

  .state-tile {
    position: relative;
    border: 2px solid white;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 900;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.1);
    transition:
      background 0.22s ease,
      color 0.22s ease,
      border 0.18s ease,
      transform 0.18s ease;
  }

  .state-tile:hover,
  .state-tile:focus,
  .state-tile.selected {
    border-color: #0f172a;
    outline: none;
    transform: translateY(-1px);
  }

  .legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem 0.85rem;
    align-items: center;
    margin-top: 0.45rem;
    color: #536173;
    font-size: 0.84rem;
  }

  .gradient-legend {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
  }

  .gradient-legend i {
    width: 145px;
    height: 0.72rem;
    border: 1px solid #cbd5e1;
    border-radius: 999px;
    background: linear-gradient(90deg, hsl(217, 76%, 94%), hsl(217, 76%, 42%));
  }

  .category-legend {
    display: inline-flex;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .category-legend span,
  .missing-key {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
  }

  .category-legend i,
  .missing-key i {
    width: 0.85rem;
    height: 0.85rem;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
  }

  .missing-key i {
    background: #e5e7eb;
  }

  dl {
    display: grid;
    gap: 0.58rem;
    margin: 0;
  }

  dl div {
    display: grid;
    gap: 0.2rem;
    padding-bottom: 0.58rem;
    border-bottom: 1px solid #e2e8f0;
  }

  dl div:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }

  dt {
    color: #64748b;
    font-size: 0.8rem;
    font-weight: 800;
  }

  dd {
    margin: 0;
    color: #172033;
    font-size: 0.92rem;
    line-height: 1.35;
  }

  .histogram-header {
    text-align: center;
  }

  .histogram-header p:not(.eyebrow) {
    margin-bottom: 0;
    color: #475569;
    font-size: 0.84rem;
    line-height: 1.25;
  }

  .histogram-svg {
    display: block;
    width: 100%;
    height: auto;
    overflow: visible;
  }

  .hist-grid {
    stroke: #e2e8f0;
    stroke-width: 1;
  }

  .hist-axis {
    stroke: #94a3b8;
    stroke-width: 1.2;
  }

  .hist-tick-label {
    fill: #64748b;
    font-size: 10px;
  }

  .hist-bar {
    fill: #93c5fd;
    transition:
      y 0.35s ease,
      height 0.35s ease,
      fill 0.25s ease;
  }

  .hist-bar.selected-bar {
    fill: #1d4ed8;
  }

  .hist-count {
    fill: #334155;
    font-size: 10px;
    font-weight: 700;
    transition: y 0.35s ease, fill 0.25s ease;
  }

  .hist-count.selected-count {
    fill: #1d4ed8;
  }

  .hist-x-label {
    fill: #475569;
    font-size: 9px;
  }

  .tooltip {
    position: fixed;
    z-index: 20;
    display: grid;
    gap: 0.2rem;
    max-width: 280px;
    padding: 0.75rem 0.85rem;
    border-radius: 14px;
    background: rgba(15, 23, 42, 0.94);
    color: white;
    pointer-events: none;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.25);
  }

  .tooltip span {
    color: #dbeafe;
    font-size: 0.8rem;
    line-height: 1.3;
  }

  @media (max-width: 1150px) {
    .content-grid {
      grid-template-columns: 1fr;
    }

    .right-column {
      grid-template-columns: 1fr 1fr;
      align-items: start;
    }

    .geo-map {
      min-width: 620px;
    }
  }

  @media (max-width: 900px) {
    .header-row,
    .right-column {
      display: grid;
      grid-template-columns: 1fr;
    }

    label {
      min-width: 0;
    }

    .geo-map {
      min-width: 560px;
    }
  }

  @media (max-width: 640px) {
    .coverage-card {
      width: 100%;
      padding: 0.9rem;
    }

    .geo-map,
    .tile-map {
      min-width: 0;
    }

    .map-summary-chip {
      max-width: 100%;
    }
  }

/* Center the full coverage component under the main page title */
.coverage-card {
  width: min(94vw, 1180px);
  margin-left: auto;
  margin-right: auto;
  transform: none;
}

/* Make sure the inner map is centered inside its card */
.map-card {
  display: grid;
  justify-items: center;
}

/* Remove any previous left/right shifting */
.geo-map,
.tile-map,
.legend {
  transform: none;
}

/* Keep the map centered within the available map card */
.geo-map {
  width: min(100%, 840px);
  min-width: 0;
  margin-left: auto;
  margin-right: auto;
}

/* Keep the legend centered below the map */
.legend {
  justify-content: center;
}

/* Nudge the whole coverage component slightly left */
.coverage-card {
  transform: translateX(-65px);
}
</style>
ALGORITHMS = {
    "g1gc": {
        "name": "G1GC",
        "label": "Garbage-First Collector",
        "color": "#00C8FF",
        "badge": "PLATFORM DEFAULT",
        "heap_model": "regions",
        "metrics": {
            "pause": "10–150 ms",
            "cpu": "MEDIUM",
            "throughput": "HIGH",
            "heap": "256 MiB – 32 GiB",
        },
        "insight": (
            "Divides heap into equal-sized regions (~1–32 MB). Selects highest-garbage "
            "regions first to achieve a configurable STW pause target via "
            "-XX:MaxGCPauseMillis. Platform default for 4 GiB / 4000m pods."
        ),
        "phases": [
            {"id": "alloc", "name": "Allocation", "ticks": 90, "stw": False, "gc_t": 0, "app_t": 4,
             "yd": [18, 72], "od": [10, 22],
             "desc": "App threads allocate objects into Eden regions. Young Gen fills progressively. "
                     "No GC overhead — no barriers, no concurrent GC threads competing for CPU."},
            {"id": "youngGC", "name": "Young GC", "ticks": 14, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [72, 16], "od": [22, 30],
             "desc": "STW pause. Eden + Survivor regions evacuated by 4 parallel GC threads. Live "
                     "objects copied to new Survivors or promoted to Old Gen."},
            {"id": "alloc2", "name": "Allocation", "ticks": 60, "stw": False, "gc_t": 0, "app_t": 4,
             "yd": [16, 58], "od": [30, 42],
             "desc": "App resumes. Fresh Eden regions fill. Old Gen accumulates promoted survivors."},
            {"id": "initMk", "name": "Initial Mark", "ticks": 6, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [58, 58], "od": [42, 42],
             "desc": "Short STW. Scans GC roots only (stack frames, statics, JNI refs). Initiates "
                     "the concurrent marking cycle."},
            {"id": "concMk", "name": "Concurrent Mark", "ticks": 60, "stw": False, "gc_t": 2, "app_t": 4,
             "yd": [58, 74], "od": [42, 49],
             "desc": "GC threads trace live objects across Old Gen concurrently. SATB write barriers "
                     "capture mutations — no objects are missed."},
            {"id": "remark", "name": "Remark", "ticks": 8, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [74, 74], "od": [49, 49],
             "desc": "Short STW. Processes SATB barrier buffers. Finalises the complete live object set."},
            {"id": "mixedGC", "name": "Mixed GC", "ticks": 18, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [74, 16], "od": [49, 24],
             "desc": "STW. Collects Young Gen + selected high-garbage Old Gen regions. Old Gen is "
                     "reclaimed incrementally across several Mixed GC cycles."},
            {"id": "cleanup", "name": "Cleanup", "ticks": 28, "stw": False, "gc_t": 1, "app_t": 4,
             "yd": [16, 28], "od": [24, 26],
             "desc": "Concurrent cleanup. Identifies empty regions, resets for reuse."},
        ],
    },
    "zgc": {
        "name": "ZGC",
        "label": "Z Garbage Collector",
        "color": "#00FF88",
        "badge": "SUB-MILLISECOND",
        "heap_model": "bars",
        "metrics": {"pause": "< 1 ms (O(1))", "cpu": "HIGH",
                     "throughput": "MEDIUM", "heap": "1 GiB – multi-TB"},
        "insight": (
            "Embeds GC metadata in pointer bits (colored pointers). Load barriers "
            "intercept every reference read, enabling fully concurrent relocation. "
            "STW pause time is constant O(1) — independent of heap size."
        ),
        "phases": [
            {"id": "alloc", "name": "Allocation", "ticks": 65, "stw": False, "gc_t": 0, "app_t": 4,
             "yd": [18, 55], "od": [10, 18],
             "desc": "App allocates. Load barriers active on every reference read — detect stale "
                     "colored pointers and self-heal transparently."},
            {"id": "markS", "name": "Mark Start", "ticks": 3, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [55, 55], "od": [18, 18],
             "desc": "PAUSE 1/3 — O(1) constant time. Scans GC roots only. Typically < 0.5 ms."},
            {"id": "concMk", "name": "Concurrent Mark", "ticks": 60, "stw": False, "gc_t": 4, "app_t": 4,
             "yd": [55, 68], "od": [18, 25],
             "desc": "Concurrent live-object tracing. Load barriers update colored pointer metadata."},
            {"id": "markE", "name": "Mark End", "ticks": 3, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [68, 68], "od": [25, 25],
             "desc": "PAUSE 2/3 — O(1). Drains marking queues. Typically < 0.5 ms."},
            {"id": "relocS", "name": "Relocate Start", "ticks": 3, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [68, 68], "od": [25, 25],
             "desc": "PAUSE 3/3 — O(1). Selects relocation set. All three pauses combined: < 2 ms."},
            {"id": "concR", "name": "Concurrent Relocate", "ticks": 55, "stw": False, "gc_t": 4, "app_t": 4,
             "yd": [68, 26], "od": [25, 12],
             "desc": "Concurrent relocation. GC moves objects; app load barriers return new addresses."},
            {"id": "remap", "name": "Concurrent Remap", "ticks": 45, "stw": False, "gc_t": 2, "app_t": 4,
             "yd": [26, 35], "od": [12, 16],
             "desc": "Updates all remaining stale heap references. Piggybacked on next mark cycle."},
        ],
    },
    "shenandoah": {
        "name": "Shenandoah",
        "label": "Shenandoah GC",
        "color": "#FFB800",
        "badge": "CONCURRENT EVAC",
        "heap_model": "bars",
        "metrics": {"pause": "< 10 ms", "cpu": "MED-HIGH",
                     "throughput": "MEDIUM", "heap": "1 GiB – 32 GiB"},
        "insight": (
            "Adds a Brooks pointer (forwarding word) to every object. GC and app "
            "threads can simultaneously access the same object at old and new locations "
            "— enabling true concurrent evacuation without load barriers in bytecode."
        ),
        "phases": [
            {"id": "alloc", "name": "Allocation", "ticks": 55, "stw": False, "gc_t": 0, "app_t": 4,
             "yd": [18, 55], "od": [10, 17],
             "desc": "App allocates into Shenandoah regions. Write barriers track mutations for SATB."},
            {"id": "initMk", "name": "Initial Mark", "ticks": 5, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [55, 55], "od": [17, 17],
             "desc": "Short STW. Scan GC roots only."},
            {"id": "concMk", "name": "Concurrent Mark", "ticks": 55, "stw": False, "gc_t": 4, "app_t": 4,
             "yd": [55, 66], "od": [17, 24],
             "desc": "Concurrent live-object tracing via SATB write barriers alongside app threads."},
            {"id": "finalMk", "name": "Final Mark", "ticks": 5, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [66, 66], "od": [24, 24],
             "desc": "Short STW. Drain SATB queues. Build collection set. Compute evacuation plan."},
            {"id": "cleanup", "name": "Concurrent Cleanup", "ticks": 12, "stw": False, "gc_t": 2, "app_t": 4,
             "yd": [66, 58], "od": [24, 20],
             "desc": "Concurrent. Immediately reclaim completely empty regions."},
            {"id": "concEv", "name": "Concurrent Evacuation", "ticks": 55, "stw": False, "gc_t": 4, "app_t": 4,
             "yd": [58, 22], "od": [20, 11],
             "desc": "KEY PHASE: Brooks pointers let GC move objects while app reads them. No STW needed."},
            {"id": "initUpd", "name": "Init Update Refs", "ticks": 3, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [22, 22], "od": [11, 11],
             "desc": "Tiny STW. Ensure all evacuation complete. Flip heap into update-refs mode."},
            {"id": "concUpd", "name": "Concurrent Update Refs", "ticks": 40, "stw": False, "gc_t": 4, "app_t": 4,
             "yd": [22, 30], "od": [11, 15],
             "desc": "Concurrent. Walk heap, update stale references to new object locations."},
            {"id": "finalUpd", "name": "Final Update Refs", "ticks": 4, "stw": True, "gc_t": 4, "app_t": 0,
             "yd": [30, 32], "od": [15, 17],
             "desc": "Short STW. Update GC roots. Reclaim old object space. Cycle complete."},
        ],
    },
    "parallelgc": {
        "name": "ParallelGC",
        "label": "Parallel Throughput Collector",
        "color": "#FF5533",
        "badge": "⚠ BATCH ONLY",
        "heap_model": "bars",
        "metrics": {"pause": "100 ms – seconds", "cpu": "LOW",
                     "throughput": "VERY HIGH", "heap": "Any"},
        "insight": (
            "All collection phases are parallel stop-the-world. Maximum CPU efficiency "
            "for batch jobs. Dangerous for HTTP services — long pauses trigger Kubernetes "
            "liveness probe failures and pod restarts under load."
        ),
        "phases": [
            {"id": "alloc", "name": "Allocation", "ticks": 65, "stw": False, "gc_t": 0, "app_t": 4,
             "yd": [18, 82], "od": [8, 16],
             "desc": "App allocates rapidly. No barriers, no concurrent GC threads. Maximum throughput."},
            {"id": "minorGC", "name": "Minor GC (STW)", "ticks": 32, "stw": True, "gc_t": 8, "app_t": 0,
             "yd": [82, 16], "od": [16, 28],
             "desc": "FULL STW. All 8 GC threads collect Young Gen in parallel. App completely suspended."},
            {"id": "alloc2", "name": "Allocation", "ticks": 80, "stw": False, "gc_t": 0, "app_t": 4,
             "yd": [16, 82], "od": [28, 68],
             "desc": "App resumes. Old Gen builds from promotions — setting up for a long major GC."},
            {"id": "majorGC", "name": "Major GC (STW)", "ticks": 90, "stw": True, "gc_t": 8, "app_t": 0,
             "yd": [82, 16], "od": [68, 16],
             "desc": "FULL STW. All 8 threads compact entire Old Gen. Duration: 100 ms–seconds. "
                     "Kubernetes liveness probes WILL fail."},
        ],
    },
    "serialgc": {
        "name": "SerialGC",
        "label": "Serial Collector",
        "color": "#9B8FFF",
        "badge": "CLI TOOLS ONLY",
        "heap_model": "bars",
        "metrics": {"pause": "Seconds", "cpu": "MINIMAL",
                     "throughput": "LOW", "heap": "< 256 MiB"},
        "insight": (
            "Single-threaded stop-the-world. Smallest GC memory footprint. "
            "Only suitable for CLI tools. Never use for Spring Boot — multi-second "
            "pauses drain connection pools and crash pods."
        ),
        "phases": [
            {"id": "alloc", "name": "Allocation", "ticks": 55, "stw": False, "gc_t": 0, "app_t": 4,
             "yd": [18, 78], "od": [8, 14],
             "desc": "App allocates. No concurrent GC activity whatsoever."},
            {"id": "minorGC", "name": "Minor GC (STW)", "ticks": 48, "stw": True, "gc_t": 1, "app_t": 0,
             "yd": [78, 20], "od": [14, 24],
             "desc": "Full STW. ONE GC thread collects Young Gen. Slower than ParallelGC."},
            {"id": "alloc2", "name": "Allocation", "ticks": 60, "stw": False, "gc_t": 0, "app_t": 4,
             "yd": [20, 78], "od": [24, 62],
             "desc": "App resumes. Nothing in background. Old Gen fills from promotions."},
            {"id": "majorGC", "name": "Major GC (STW)", "ticks": 120, "stw": True, "gc_t": 1, "app_t": 0,
             "yd": [78, 20], "od": [62, 20],
             "desc": "Full STW. ONE thread marks and compacts entire Old Gen. Potentially several "
                     "seconds of complete application freeze."},
        ],
    },
}

G1_LAYOUTS = {
    "alloc":   [0,0,0,4,4, 0,0,4,4,4, 2,2,2,3,4, 1,1,2,2,4],
    "youngGC": [5,5,5,4,4, 5,5,4,4,4, 2,2,2,3,4, 5,5,2,2,4],
    "alloc2":  [0,0,0,0,4, 0,0,4,4,4, 2,2,2,3,4, 1,1,2,2,4],
    "initMk":  [0,0,0,0,4, 0,0,4,4,4, 6,2,2,3,4, 1,1,6,2,4],
    "concMk":  [0,0,0,0,4, 0,0,4,4,4, 6,6,6,3,4, 1,1,6,6,4],
    "remark":  [0,0,0,0,4, 0,0,4,4,4, 6,6,6,3,4, 1,1,6,6,4],
    "mixedGC": [5,5,5,5,4, 5,5,4,4,4, 5,5,2,3,4, 5,5,5,2,4],
    "cleanup": [0,0,4,4,4, 0,0,4,4,4, 2,2,2,3,4, 1,1,2,2,4],
}

REGION_TYPE_CFG = {
    0: {"label": "E", "name": "Eden",       "fill": "rgba(0,136,255,0.27)",   "border": "#0088FF"},
    1: {"label": "S", "name": "Survivor",   "fill": "rgba(255,215,0,0.27)",   "border": "#FFD700"},
    2: {"label": "O", "name": "Old",        "fill": "rgba(124,77,255,0.27)",  "border": "#7C4DFF"},
    3: {"label": "H", "name": "Humongous",  "fill": "rgba(255,109,0,0.27)",   "border": "#FF6D00"},
    4: {"label": "·", "name": "Free",       "fill": "rgba(4,8,16,0.27)",      "border": "#0F1E2E"},
    5: {"label": "C", "name": "Collecting", "fill": "rgba(255,23,68,0.27)",   "border": "#FF1744"},
    6: {"label": "M", "name": "Marking",    "fill": "rgba(0,255,136,0.27)",   "border": "#00FF88"},
}

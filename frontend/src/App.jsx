import { useState, useEffect } from 'react';
import './App.css';
import { MAX_BATCH_ITEMS } from './config';
import Login from './Login';
// Imported from JSON
import TEMPLATES from './templates.json';

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [type, setType] = useState('beam');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState(null);
    const [error, setError] = useState(null);
    const [isBatch, setIsBatch] = useState(false);

    // Initial default params - Empty for manual entry
    const defaultBeam = { H: '', B: '', tw: '', tf: '' };
    const defaultCol = { width: '', height: '' };

    // Single Mode Param State
    const [singleParams, setSingleParams] = useState(defaultBeam);

    // Batch Mode Params State (Array of objects)
    const [batchItems, setBatchItems] = useState([defaultBeam, defaultBeam]);

    // Template Data
    const [templates, setTemplates] = useState(() => {
        const saved = localStorage.getItem('dxf_templates');
        return saved ? JSON.parse(saved) : TEMPLATES;
    });

    // Save templates to localStorage whenever they change
    useEffect(() => {
        localStorage.setItem('dxf_templates', JSON.stringify(templates));
    }, [templates]);

    const [showTemplates, setShowTemplates] = useState(false);

    // Sync params when type changes
    useEffect(() => {
        const def = type === 'beam' ? defaultBeam : defaultCol;
        setSingleParams(def);
        setBatchItems([def, def]);
    }, [type]);

    // Auto-clear error after 6 seconds
    useEffect(() => {
        if (error) {
            const timer = setTimeout(() => {
                setError(null);
            }, 6000);
            return () => clearTimeout(timer);
        }
    }, [error]);

    if (!isLoggedIn) {
        return <Login onLogin={() => setIsLoggedIn(true)} />;
    }

    const handleSingleChange = (e) => {
        setSingleParams({ ...singleParams, [e.target.name]: e.target.value });
    };

    const handleBatchChange = (index, e) => {
        const newItems = [...batchItems];
        newItems[index] = { ...newItems[index], [e.target.name]: e.target.value };
        setBatchItems(newItems);
    };

    const addBatchItem = () => {
        if (batchItems.length < MAX_BATCH_ITEMS) {
            setBatchItems([...batchItems, type === 'beam' ? defaultBeam : defaultCol]);
        }
    };

    const removeBatchItem = (index) => {
        if (batchItems.length > 1) {
            const newItems = batchItems.filter((_, i) => i !== index);
            setBatchItems(newItems);
        }
    };

    const parseParams = (params) => {
        const parsed = {};
        for (const key in params) {
            const val = parseFloat(params[key]);
            if (isNaN(val)) throw new Error(`Invalid value for ${key}`);
            if (val < 0) throw new Error(`Value for ${key} cannot be negative`);
            parsed[key] = val;
        }
        return parsed;
    };

    const generateOneList = async (rawParams, index) => {
        const params = parseParams(rawParams);
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ component_type: type, params })
        });

        if (!response.ok) {
            let errorMessage = 'Generation failed';
            try {
                const errData = await response.json();
                errorMessage = errData.detail || errorMessage;
            } catch (e) {
                // If response is not JSON, use the status text
                errorMessage = `Error ${response.status}: ${response.statusText || 'Server Error'}`;
            }
            throw new Error(errorMessage);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${type}_${index !== undefined ? index + 1 : 'generated'}.dxf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    };

    const generateDXF = async () => {
        setLoading(true);
        setError(null);
        setMessage(null);

        try {
            if (isBatch) {
                // Validate all first
                batchItems.forEach(p => parseParams(p));

                // Sequential Requests with Delay
                let successCount = 0;
                for (let i = 0; i < batchItems.length; i++) {
                    await generateOneList(batchItems[i], i);
                    successCount++;
                    // Add small delay to allow browser to process download
                    if (i < batchItems.length - 1) {
                        await new Promise(resolve => setTimeout(resolve, 500));
                    }
                }
                setMessage(`Successfully generated ${successCount} files.`);
                setTimeout(() => setMessage(null), 5000);
            } else {
                await generateOneList(singleParams);
                setMessage("DXF Generated and Downloaded Successfully!");
                setTimeout(() => setMessage(null), 5000);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };


    const renderInputs = (params, onChange, index = null) => {
        if (type === 'beam') {
            return (
                <div className="batch-grid-beam">
                    <input type="number" name="H" placeholder="H" value={params.H} onChange={onChange} title="Depth" />
                    <input type="number" name="B" placeholder="B" value={params.B} onChange={onChange} title="Width" />
                    <input type="number" name="tw" placeholder="tw" value={params.tw} onChange={onChange} title="Web Thk" />
                    <input type="number" name="tf" placeholder="tf" value={params.tf} onChange={onChange} title="Flng Thk" />
                    {index !== null && batchItems.length > 1 && (
                        <button onClick={() => removeBatchItem(index)} className="btn-remove" title="Remove">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <polyline points="3 6 5 6 21 6"></polyline>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            </svg>
                        </button>
                    )}
                </div>
            );
        } else {
            return (
                <div className="batch-grid-col">
                    <input type="number" name="width" placeholder="Width" value={params.width} onChange={onChange} />
                    <input type="number" name="height" placeholder="Height" value={params.height} onChange={onChange} />
                    {index !== null && batchItems.length > 1 && (
                        <button onClick={() => removeBatchItem(index)} className="btn-remove" title="Remove">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <polyline points="3 6 5 6 21 6"></polyline>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                            </svg>
                        </button>
                    )}
                </div>
            );
        }
    };

    // Template Data moved to top

    const handleTemplateParamChange = (templateId, paramName, value) => {
        setTemplates(prev => prev.map(t => {
            if (t.id === templateId) {
                return {
                    ...t,
                    params: { ...t.params, [paramName]: value }
                };
            }
            return t;
        }));
    };

    const handleLoadTemplate = (template) => {
        const typeChanged = type !== template.type;
        setType(template.type);
        if (isBatch) {
            // In batch mode, append as a new item
            if (batchItems.length < MAX_BATCH_ITEMS) {
                // If type changed, we should probably clear the old batch items of different type or handle it
                // For now, let's just append. The render logic handles type consistency.
                setBatchItems(prev => [...prev, template.params]);
                setMessage(`Loaded "${template.name}" into batch list.`);
                setTimeout(() => setMessage(null), 3000);
            } else {
                setError("Batch limit reached! Cannot add template.");
                setTimeout(() => setError(null), 3000);
            }
        } else {
            // Single mode - replace current params
            setSingleParams(template.params);
            setMessage(`Loaded "${template.name}" configuration.`);
            setTimeout(() => setMessage(null), 3000);
        }
        setShowTemplates(false);
    };

    const handleSaveAsTemplate = () => {
        const name = prompt("Enter a name for this template:");
        if (!name) return;

        const newTemplate = {
            id: Date.now(),
            name: name,
            type: type,
            params: isBatch ? batchItems[0] : singleParams // Save first item if batch
        };

        setTemplates(prev => [...prev, newTemplate]);
        setMessage(`Saved "${name}" as a new template.`);
        setTimeout(() => setMessage(null), 3000);
    };

    const handleDeleteTemplate = (id, e) => {
        e.stopPropagation();
        if (window.confirm("Delete this template?")) {
            setTemplates(prev => prev.filter(t => t.id !== id));
        }
    };

    const handleResetTemplates = () => {
        if (window.confirm("Reset all templates to default? This will delete your custom ones.")) {
            setTemplates(TEMPLATES);
        }
    };

    const handleUploadDXF = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/parse-dxf', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                let errorMessage = 'Failed to parse DXF';
                try {
                    const data = await response.json();
                    errorMessage = data.detail || errorMessage;
                } catch (e) {
                    errorMessage = `Error ${response.status}: ${response.statusText || 'Server Error'}`;
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();
            
            // Switch type if necessary
            if (data.type !== type) {
                setType(data.type);
            }

            // Auto-fill params
            setSingleParams(data.params);
            
            setMessage(`Successfully extracted ${data.type} data from DXF.`);
            setTimeout(() => setMessage(null), 3000);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
            e.target.value = ''; // Reset input
        }
    };

    const handleLogout = () => {
        setIsLoggedIn(false);
        // Optional: Reset other states if needed
        setIsBatch(false);
        setType('beam');
    };

    return (
        <div className="app-wrapper">
            {showTemplates && (
                <div className="modal-overlay" onClick={() => setShowTemplates(false)}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <h2>Select Templates</h2>
                            <div className="modal-actions">
                                <button className="btn-save-new-template" onClick={handleSaveAsTemplate}>
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                                        <polyline points="17 21 17 13 7 13 7 21"></polyline>
                                        <polyline points="7 3 7 8 15 8"></polyline>
                                    </svg>
                                    Save Template
                                </button>
                                <button className="btn-reset-templates" onClick={handleResetTemplates}>Reset</button>
                                <button className="btn-close" onClick={() => setShowTemplates(false)}>×</button>
                            </div>
                        </div>
                        <div className="template-grid">
                            {templates.map(t => (
                                <div key={t.id} className="template-card">
                                    <div className="template-header-row" onClick={() => handleLoadTemplate(t)}>
                                        <div className="template-icon">
                                            {t.type === 'beam' ? 'I' : '⛶'}
                                        </div>
                                        <div className="template-info">
                                            <h3>{t.name}</h3>
                                        </div>
                                        <div className="template-right-controls">
                                            {t.id > 1000 && (
                                                <button className="btn-delete-template" onClick={(e) => handleDeleteTemplate(t.id, e)} title="Delete Template">
                                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                        <polyline points="3 6 5 6 21 6"></polyline>
                                                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                                                    </svg>
                                                </button>
                                            )}
                                            <div className="template-load-badge">Click to Load</div>
                                        </div>
                                    </div>
                                    <div className="template-edit-controls">
                                        {t.type === 'beam' ? (
                                            <>
                                                <div className="mini-input"><span>H</span><input type="number" value={t.params.H} onChange={(e) => handleTemplateParamChange(t.id, 'H', e.target.value)} onClick={e => e.stopPropagation()} /></div>
                                                <div className="mini-input"><span>B</span><input type="number" value={t.params.B} onChange={(e) => handleTemplateParamChange(t.id, 'B', e.target.value)} onClick={e => e.stopPropagation()} /></div>
                                                <div className="mini-input"><span>tw</span><input type="number" value={t.params.tw} onChange={(e) => handleTemplateParamChange(t.id, 'tw', e.target.value)} onClick={e => e.stopPropagation()} /></div>
                                                <div className="mini-input"><span>tf</span><input type="number" value={t.params.tf} onChange={(e) => handleTemplateParamChange(t.id, 'tf', e.target.value)} onClick={e => e.stopPropagation()} /></div>
                                            </>
                                        ) : (
                                            <>
                                                <div className="mini-input"><span>W</span><input type="number" value={t.params.width} onChange={(e) => handleTemplateParamChange(t.id, 'width', e.target.value)} onClick={e => e.stopPropagation()} /></div>
                                                <div className="mini-input"><span>H</span><input type="number" value={t.params.height} onChange={(e) => handleTemplateParamChange(t.id, 'height', e.target.value)} onClick={e => e.stopPropagation()} /></div>
                                            </>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}

            <nav className="top-navbar">
                <div className="nav-brand"></div> {/* Spacer or Brand if needed */}
                <button className="nav-item btn-template-nav" onClick={() => setShowTemplates(true)}>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                    <span>Templates</span>
                </button>
                <button className="nav-item btn-logout-nav" onClick={handleLogout}>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                        <polyline points="16 17 21 12 16 7"></polyline>
                        <line x1="21" y1="12" x2="9" y2="12"></line>
                    </svg>
                    <span>Logout</span>
                </button>
            </nav>

            <div className={`container ${isBatch ? 'container-batch' : ''}`}>
                <h1>DXF Generator</h1>

                <div className="tabs">
                    <div className={`tab ${type === 'beam' ? 'active' : ''}`} onClick={() => setType('beam')}>I-Beam</div>
                    <div className={`tab ${type === 'column' ? 'active' : ''}`} onClick={() => setType('column')}>Column</div>
                </div>

                <div className="form-group checkbox-group">
                    <label>
                        <input
                            type="checkbox"
                            checked={isBatch}
                            onChange={(e) => setIsBatch(e.target.checked)}
                        />
                        Batch Generation Mode (Multi-Value)
                    </label>
                </div>

                {!isBatch && (
                    <div className="upload-dxf-section">
                        <label className="btn-upload-dxf">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                <polyline points="17 8 12 3 7 8"></polyline>
                                <line x1="12" y1="3" x2="12" y2="15"></line>
                            </svg>
                            Upload DXF to Edit
                            <input type="file" accept=".dxf" onChange={handleUploadDXF} style={{ display: 'none' }} />
                        </label>
                        <p className="upload-hint">Upload an existing DXF to auto-fill these values</p>
                    </div>
                )}

                {!isBatch ? (
                    <div>
                        {type === 'beam' ? (
                            <>
                                <div className="form-group"><label>Total Depth (H)</label><input type="number" name="H" placeholder="H" value={singleParams.H} onChange={handleSingleChange} /></div>
                                <div className="form-group"><label>Flange Width (B)</label><input type="number" name="B" placeholder="B" value={singleParams.B} onChange={handleSingleChange} /></div>
                                <div className="form-group"><label>Web Thickness (tw)</label><input type="number" name="tw" placeholder="tw" value={singleParams.tw} onChange={handleSingleChange} /></div>
                                <div className="form-group"><label>Flange Thickness (tf)</label><input type="number" name="tf" placeholder="tf" value={singleParams.tf} onChange={handleSingleChange} /></div>
                            </>
                        ) : (
                            <>
                                <div className="form-group"><label>Width</label><input type="number" name="width" placeholder="Width" value={singleParams.width} onChange={handleSingleChange} /></div>
                                <div className="form-group"><label>Height</label><input type="number" name="height" placeholder="Height" value={singleParams.height} onChange={handleSingleChange} /></div>
                            </>
                        )}
                    </div>
                ) : (
                    <div>
                        <div className="batch-container">
                            {/* Header Row */}
                            {type === 'beam' ? (
                                <div className="batch-grid-beam">
                                    <div className="grid-header">Total Depth (H)</div>
                                    <div className="grid-header">Flange Width (B)</div>
                                    <div className="grid-header">Web Thk (tw)</div>
                                    <div className="grid-header">Flange Thk (tf)</div>
                                    <div></div> {/* Remove spacer */}
                                </div>
                            ) : (
                                <div className="batch-grid-col">
                                    <div className="grid-header">Width</div>
                                    <div className="grid-header">Height</div>
                                    <div></div>
                                </div>
                            )}

                            {/* Input Rows */}
                            {batchItems.map((item, idx) => (
                                <div key={idx}>
                                    {renderInputs(item, (e) => handleBatchChange(idx, e), idx)}
                                </div>
                            ))}
                        </div>
                        <button onClick={addBatchItem} className="btn-add" disabled={batchItems.length >= MAX_BATCH_ITEMS}>
                            {batchItems.length >= MAX_BATCH_ITEMS ? `Max Limit Reached (${MAX_BATCH_ITEMS})` : '+ Add Item'}
                        </button>
                    </div>
                )}

                <button onClick={generateDXF} disabled={loading} className="btn-generate">
                    {loading ? 'Generating...' : (isBatch ? `Generate ${batchItems.length} Files` : 'Generate DXF')}
                </button>

                {message && <div className="success">{message}</div>}
                {error && <div className="error">{error}</div>}
            </div>
        </div>
    );
}

export default App;

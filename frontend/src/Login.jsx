import { useState } from 'react';

const Login = ({ onLogin }) => {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        // Hardcoded credentials as requested
        if (email === 'user' && password === 'user') {
            onLogin();
        } else {
            setError('Invalid credentials. Please use "user" for both fields.');
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2>{isLogin ? 'Login' : 'Sign Up'} to DXF Generate</h2>
                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <span className="icon">✉️</span>
                        <input
                            type="text"
                            placeholder="Username / Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <span className="icon">🔒</span>
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    {error && <div style={{ color: 'red', marginTop: '10px', fontSize: '0.9rem' }}>{error}</div>}

                    {isLogin && <a href="#" className="forgot-password">Forgot Password?</a>}

                    <button type="submit" className="btn-login">
                        {isLogin ? 'Login' : 'Sign Up'}
                    </button>

                    <div style={{ marginTop: '1.5rem', fontSize: '0.9rem', color: '#666' }}>
                        {isLogin ? "Don't have an account? " : "Already have an account? "}
                        <span
                            onClick={() => setIsLogin(!isLogin)}
                            style={{ color: '#007bff', cursor: 'pointer', fontWeight: 'bold' }}
                        >
                            {isLogin ? 'Sign Up' : 'Login'}
                        </span>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;

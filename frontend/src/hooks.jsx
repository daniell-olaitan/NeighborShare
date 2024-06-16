import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../config.js';

export function useForeground() {
    const [isForegroundOpen, setIsForegroundOpen] = useState(false);

    const openForeground = () => {
        setIsForegroundOpen(true);
        document.body.style.overflow = 'hidden';
    };
    const closeForeground = () => {
        setIsForegroundOpen(false);
        document.body.style.overflow = 'auto';
    };

    return [ isForegroundOpen, openForeground, closeForeground ];
}

export function useAuth() {
    const baseUrl = `${API_BASE_URL}/auth`;
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        try {
            const accessToken = localStorage.getItem('accessToken');
            const refreshToken = localStorage.getItem('refreshToken');
            if (accessToken) {
                fetch(`${baseUrl}/check-login-status`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${accessToken}`,
                    },
                })
                .then((response) => {
                    if (response.status === 200) return response.json();
                })
                .then((response) => {
                    if (response.success) setIsAuthenticated(true);
                })
                .catch((error) => setIsAuthenticated(false))
            } else if (refreshToken) {
                fetch(`${baseUrl}/refresh-token`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${refreshToken}`,
                    },
                })
                .then((response) => {
                    if (response.status === 200) {
                            return response.json()
                        } else {
                            setIsAuthenticated(false);
                            throw new Error();
                        }
                })
                .then((response) => {
                    localStorage.setItem('accessToken', response.accessToken)
                    fetch(`${baseUrl}/check-login-status`, {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${response.accessToken}`,
                        },
                    })
                    .then((response) => {
                        if (response.status === 200)setIsAuthenticated(true);
                            else setIsAuthenticated(false);
                        }).catch((error) => setIsAuthenticated(false))
                    })
                    .then((response) => {
                        if (response.status === 200) return response.json();
                    })
                    .then((response) => {
                        if (response.success) setIsAuthenticated(true);
                        else setIsAuthenticated(false);
                    })
                    .catch((error) => setIsAuthenticated(false))
            } else setIsAuthenticated(false);
        } catch (error) {
            setIsAuthenticated(false);
        } finally {
            setIsLoading(false);
        }
    }, [])

    return [isAuthenticated, isLoading, setIsLoading]
}

import { AuthHeading, InputField, Modal, LoadingSpinner } from './utils.jsx';
import { formStyle, bodyStyle, buttonStyle, linkStyle } from './utils.jsx';
import { useForm } from 'react-hook-form';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useForeground, useAuth } from '../hooks.jsx';
import { useState, useEffect } from 'react';
import { API_BASE_URL } from '../../config.js';

function AuthHeader() {
    return (
        <div className="flex flex-col items-center gap-2">
            <Link to='/home' className="text-3xl font-bold">NeighborShare</Link>
            <p className="font-thin tracting-wider">Connect with your neighbors and share resources</p>
        </div>
    );
}

function SignIn() {
    const navigate = useNavigate()
    const [response, setResponse] = useState({});
    const [error, setError] = useState(null);
    const { handleSubmit, register, formState: { errors } } = useForm();
    const [isSpinnerOpen, openSpinner, closeSpinner] = useForeground();
    const [isModalOpen, openModal, closeModal] = useForeground();
    const [isAuthenticated, isLoading, setIsLoading] = useAuth();

    useEffect(() => {
        if(isLoading) {
            openSpinner();
        } else {
            closeSpinner();
        }
    }, [isLoading]);

    useEffect(() => {
        if (Object.keys(response).length !== 0) {
            if (response.hasOwnProperty('error')) {
                openModal();
            } else {
                closeModal();
                if (response.hasOwnProperty('accessToken')) {
                    localStorage.setItem('accessToken', response.accessToken);
                    localStorage.setItem('refreshToken', response.refreshToken);
                    navigate('/home');
                }
            }
        }
    }, [response]);

    useEffect(() => {
        if (isAuthenticated) navigate('/home');
    }, [isAuthenticated])

    const onSubmit = function (data, event) {
        event.preventDefault();
        setIsLoading(true);

        fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then((response) => {
                if (response.status >= 400) {
                    throw new Error('server error');
                }

                return response.json();
            })
            .then ((response) => setResponse(response))
            .catch((error) => setError(error))
            .finally(() => setIsLoading(false));
    }

    if (error) return <p>A network error was encountered.</p>;

    return (
        <div  className={bodyStyle()}>
            <LoadingSpinner isOpen={isSpinnerOpen} />
            <Modal isOpen={isModalOpen} onClose={closeModal} header='error' >
                <p>{response.error}</p>
            </Modal>
            <AuthHeader />
        <form className={formStyle()} onSubmit={handleSubmit(onSubmit)}>
            <AuthHeading text="Sign in to NeighborShare"/>
            <InputField type="email" label="email" error={errors.email}
                errorMessage="email is required and must be correct"
                rules={{patttern: /^\S+@\S+$/i, required: true}} name="email" register={register}
            />
            <InputField type="password" label="password" error={errors.password}
                errorMessage="password is required" rules={{required: true}}
                name="password" register={register}
            />
            <button className={buttonStyle()} type="submit">sign in</button>
            <div className="flex flex-row pb-6 mb-4 border-b border-gray-400">
                <Link to='/reset-password' className={linkStyle() + " ml-auto"}>
                    forgotten password?
                </Link>
            </div>
                <Link to='/sign-in' className={buttonStyle() + ' text-center w-full mb-4'}>sign in as a demo user</Link>
                <Link to='/sign-up' className={buttonStyle() + ' text-center w-full'}>create new account</Link>
        </form>
        </div>
    );
}

function SignUp() {
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const [response, setResponse] = useState({});
    const { handleSubmit, register, formState: { errors }, getValues } = useForm();
    const [isSpinnerOpen, openSpinner, closeSpinner] = useForeground();
    const [isModalOpen, openModal, closeModal] = useForeground();
    const [isAuthenticated, isLoading, setIsLoading] = useAuth();
    const [header, setHeader] = useState('');
    const [message, setMessage] = useState('');

    const modalClose = function () {
        closeModal();
        navigate('/sign-in');
    };

    useEffect(() => {
        if(isLoading) {
            openSpinner();
        } else {
            closeSpinner();
        }
    }, [isLoading]);

    useEffect(() => {
        if (Object.keys(response).length !== 0) {
            let headr;
            let msg;
            if (response.success) {
                msg = 'A confirmation link has been sent to your email. The link expires in 10 minutes';
                headr = 'success';
            } else {
                headr = 'error';
                msg = response.error;
            }
            setMessage(msg);
            setHeader(headr);
            openModal();
        }
    }, [response]);

    useEffect(() => {
        if (isAuthenticated) navigate('/home');
    }, [isAuthenticated])

    const onSubmit = function (data, event) {
        event.preventDefault();
        setIsLoading(true);

        fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then((response) => {
                if (response.status >= 400) {
                    throw new Error('server error');
                }

                return response.json();
            })
            .then ((response) => {
                setResponse(response);
            })
            .catch((error) => setError(error))
            .finally(() => setIsLoading(false));
    };

    if (error) return <p>A network error was encountered.</p>;

    return (
        <div  className={bodyStyle()}>
            <LoadingSpinner isOpen={isSpinnerOpen} />
            <Modal isOpen={isModalOpen} onClose={modalClose} header={header} >
                <p>{message}</p>
            </Modal>
            <AuthHeader />
        <form className={formStyle()} onSubmit={handleSubmit(onSubmit)}>
            <AuthHeading text="Create a free account"/>
            <InputField type="text" label="username" error={errors.username}
                errorMessage="usernames must have only letters, numbers, dots or underscores"
                rules={{pattern: /^[A-Za-z][A-Za-z0-9_.]*$/i, required: true}} name="username"
                register={register}
            />
            <InputField type="email" label="email" error={errors.email}
                errorMessage="email is required and must be correct"
                rules={{patttern: /^\S+@\S+$/i, required: true}} name="email" register={register}
            />
            <InputField type="password"  error={errors.password} label="password" name="password" register={register}
                rules={{required: true, pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,16}$/}}
                errorMessage="password must be minimum 8, maximum 16, at least 1 lowercase, 1 uppercase, 1 number, 1 special case [._@])"
            />
            <InputField type="password" label="confirm password" error={errors.confirmPassword} errorMessage="password does not match"
                name="confirmPassword" register={register} rules={{validate: (value) => value === getValues('password'), required: true}}
            />
            <div className="flex flex-row mb-6">
                <p>Already have an account?</p>
                <Link className={linkStyle() + " ml-auto"} to='/sign-in'>sign in</Link>
            </div>
            <button className={buttonStyle() + " w-full"}>sign up</button>
        </form>
        </div>
    );
}

function Confirmation({status, type, successMessage, failedMessage}) {
    const navigate = useNavigate();
    const [isModalOpen, openModal, closeModal] = useForeground();
    const [isAuthenticated, isLoading, setIsLoading] = useAuth();
    const [message, setMessage] = useState('');

    useEffect(() => {
        if (isAuthenticated) navigate('/home');
    }, [isAuthenticated])

    const modalClose = function () {
        closeModal();
        if (type === 'password') {
            if (status === 'success') navigate('/create-password');
            else if (status === 'error') navigate('/reset-password');
        } else if (type === 'email') navigate('/sign-in');
    };

    useEffect(() => {
        if (status === 'success') {
            setMessage(successMessage);
        } else if(status === 'error') {
            setMessage(failedMessage);
        }
        openModal();
    }, []);

    return (
        <div  className={bodyStyle()}>
            <Modal isOpen={isModalOpen} onClose={modalClose} header={status} >
                <p>{message}</p>
            </Modal>
        </div>
    );
}

function EmailConfirmation() {
    const { status } = useParams();
    const failedMessage = 'The confirmation link is invalid, has expired or you have already confirmed your account.';
    const successMessage = 'You have successfully confirmed your account. Proceed to log in';

    return <Confirmation status={status} type='email' successMessage={successMessage} failedMessage={failedMessage} />
}

function PasswordConfirmation() {
    const { status } = useParams();
    const successMessage = 'Proceed to change your password';
    const failedMessage = 'The confirmation link is invalid or has expired.';

    return <Confirmation status={status} type='password' successMessage={successMessage} failedMessage={failedMessage} />
}

function ResetPasswordPage() {
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const { handleSubmit, register, formState: { errors } } = useForm();
    const [isSpinnerOpen, openSpinner, closeSpinner] = useForeground();
    const [isModalOpen, openModal, closeModal] = useForeground();
    const [isAuthenticated, isLoading, setIsLoading] = useAuth();
    const [header, setHeader] = useState('');
    const [message, setMessage] = useState('');

    useEffect(() => {
        if (isAuthenticated) navigate('/home');
    }, [isAuthenticated])

    const modalClose = function () {
        closeModal();
        navigate('/sign-in');
    };

    useEffect(() => {
        if(isLoading) {
            openSpinner();
        } else {
            closeSpinner();
        }
    }, [isLoading]);

    const onSubmit = function (data, event) {
        event.preventDefault();
        setIsLoading(true);

        fetch(`${API_BASE_URL}/auth/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then((response) => {
                if (response.status >= 400) {
                    throw new Error('server error');
                }

                return response.json();
            })
            .then ((response) => {
                if (response.success) {
                    setMessage('A confirmation link has been sent to your mail. The link will expire in 10 minutes');
                    setHeader('success');
                } else if (response.error) {
                    setMessage(response.error);
                    setHeader('error');
                }
                openModal();
            })
            .catch((error) => setError(error))
            .finally(() => setIsLoading(false));
        }

    if (error) return <p>A network error was encountered.</p>;

    return (
        <div  className={bodyStyle()}>
            <LoadingSpinner isOpen={isSpinnerOpen} />
            <Modal isOpen={isModalOpen} onClose={modalClose} header={header} >
                <p>{message}</p>
            </Modal>
            <AuthHeader />
        <form className={formStyle()} onSubmit={handleSubmit(onSubmit)}>
            <AuthHeading text="Input your email"/>
            <InputField type="email" label="email" error={errors.email}
                errorMessage="email is required and must be correct"
                rules={{patttern: /^\S+@\S+$/i, required: true}} name="email" register={register}
            />

            <button className={buttonStyle()} type="submit">submit</button>
                <Link to='/sign-in' className={buttonStyle() + ' mt-10 text-center w-full mb-4'}>sign in</Link>
                <Link to='/sign-up' className={buttonStyle() + ' text-center w-full'}>sign up</Link>
        </form>
        </div>
    );
}

function NewPasswordPage() {
    const navigate = useNavigate();
    const [error, setError] = useState(null);
    const { handleSubmit, register, formState: { errors }, getValues } = useForm();
    const [isSpinnerOpen, openSpinner, closeSpinner] = useForeground();
    const [isModalOpen, openModal, closeModal] = useForeground();
    const [isAuthenticated, isLoading, setIsLoading] = useAuth();
    const [header, setHeader] = useState('');
    const [message, setMessage] = useState('');

    useEffect(() => {
        if (isAuthenticated) navigate('/home');
    }, [isAuthenticated])

    const modalClose = function () {
        closeModal();
        navigate('/sign-in');
    };

    useEffect(() => {
        if(isLoading) {
            openSpinner();
        } else {
            closeSpinner();
        }
    }, [isLoading]);

    const onSubmit = function (data, event) {
        event.preventDefault();
        setIsLoading(true);

        fetch(`${API_BASE_URL}/auth/password-reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
            .then((response) => {
                if (response.status >= 400) {
                    throw new Error('server error');
                }

                return response.json();
            })
            .then ((response) => {
                if (response.success) {
                    setMessage('You have successfully changed your password. Proceed to log in.');
                    setHeader('success');
                } else if (response.error) {
                    setMessage(response.error);
                    setHeader('error');
                }
                openModal();
            })
            .catch((error) => setError(error))
            .finally(() => setIsLoading(false));
        }

    if (error) return <p>A network error was encountered.</p>;

    return (
        <div  className={bodyStyle()}>
            <LoadingSpinner isOpen={isSpinnerOpen} />
            <Modal isOpen={isModalOpen} onClose={modalClose} header={header} >
                <p>{message}</p>
            </Modal>
            <AuthHeader />
        <form className={formStyle()} onSubmit={handleSubmit(onSubmit)}>
            <AuthHeading text="Create a new password"/>
            <InputField type="email" label="email" error={errors.email}
                errorMessage="email is required and must be correct"
                rules={{patttern: /^\S+@\S+$/i, required: true}} name="email" register={register}
            />
            <InputField type="password"  error={errors.password} label="new password" name="password" register={register}
                rules={{required: true, pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,16}$/}}
                errorMessage="password must be minimum 8, maximum 16, at least 1 lowercase, 1 uppercase, 1 number, 1 special case [._@])"
            />
            <InputField type="password" label="confirm password" error={errors.confirmPassword} errorMessage="password does not match"
                name="confirmPassword" register={register} rules={{validate: (value) => value === getValues('password'), required: true}}
            />

            <button className={buttonStyle()} type="submit">submit</button>
                <Link to='/sign-in' className={buttonStyle() + ' mt-10 text-center w-full mb-4'}>sign in</Link>
                <Link to='/sign-up' className={buttonStyle() + ' text-center w-full'}>sign up</Link>
        </form>
        </div>
    );
}

export { SignIn, SignUp, PasswordConfirmation, EmailConfirmation, ResetPasswordPage, NewPasswordPage};

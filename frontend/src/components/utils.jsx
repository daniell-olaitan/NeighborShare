import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Icon from '@mdi/react';
import { mdiClose, mdiMenu } from '@mdi/js';
import { useAuth } from '../hooks.jsx';
import { API_BASE_URL } from '../../config.js';
import { useNavigate } from 'react-router-dom';


export function formStyle() {
    return 'flex flex-col gap-4 bg-gray-200 p-10 w-1/3'
}

export function headingStyle() {
    return 'text-3xl font-light my-10 ml-32'
}

export function bodyStyle() {
    return 'flex flex-row justify-center gap-20 items-center h-screen';
}

export function buttonStyle() {
    return 'font-semibold bg-black text-white py-3 rounded-lg hover:bg-gray-500';
}

export function linkStyle() {
    return 'underline';
}

export function AuthHeading(props) {
    return <p className='text-xl font-semibold mb-6'>{props.text}</p>
}

export function InputField(props) {
    const errorStyle = {
        color: 'red'
    };

    return (
        <div>
            <label className="text-lg w-full" style={{display: 'inline-block'}} htmlFor={props.name}>{props.label}</label>
            <input className="w-full bg-gray-50 h-8 p-2" type={props.type} { ...props.register(props.name, props.rules) }/>
            {props.error && <p style={errorStyle}>{props.errorMessage}</p>}
        </div>
    );
}

export function Header({ selected }) {
    let links = {};
    let navItems = [];
    const [navStatus, setNavStatus] = useState(true);
    const [isAuthenticated, isLoading, setIsLoading] = useAuth();
    const [user, setUser] = useState({username: 'A'});
    const navigate = useNavigate();
    const button1Ref = useRef(null);
    const button2Ref = useRef(null);
    const navRef = useRef(null);
    const [error, setError] = useState(null);
    const navStyle = 'font-thin tracking-wider hover:underline';
    const selectedStyle = 'underline font-semibold';

    useEffect(() => {
        if (isAuthenticated) {
            const token = localStorage.getItem('accessToken');
            fetch(`${API_BASE_URL}/auth/get-current-user`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            })
            .then((response) => {
                if (response.status >= 400) throw new Error('server error')

                return response.json();
            })
            .then((response) => {
                if (response.user) setUser(response.user);
                else throw new Error();
            })
            .catch((error) => console.log(error))
        }
    }, [isAuthenticated])

    const handleLogOut = function (event) {
        event.preventDefault();
        const token = localStorage.getItem('accessToken');
        fetch(`${API_BASE_URL}/auth/logout`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        })
        .then((response) => {
            if (response.status >= 400) throw new Error('server error')

            return response.json();
        })
        .then((response) => {
            console.log(response.success);
            if (response.success) navigate('/sign-in');
            else throw new Error();
        })
        .catch((error) => console.log(error))
    };

    const handleNav = function (event) {
        event.preventDefault();
        if (navStatus) {
            button1Ref.current.classList.add('hidden');
            button1Ref.current.classList.remove('block');
            button2Ref.current.classList.remove('hidden');
            button2Ref.current.classList.add('block');
            navRef.current.classList.add('block');
            navRef.current.classList.remove('hidden');
            setNavStatus(false);
        } else {
            button1Ref.current.classList.remove('hidden');
            button1Ref.current.classList.add('block');
            button2Ref.current.classList.add('hidden');
            button2Ref.current.classList.remove('block');
            navRef.current.classList.add('hidden');
            navRef.current.classList.remove('block');
            setNavStatus(true);
        }
    };

    if (isAuthenticated) {
        navItems = ['Home', 'My Resources', 'My Interests', 'Add Resource', 'Requests', 'Chats'];
        links = {
           Home: '/home',
            'My Resources': '/my-resources',
            'My Interests': '/my-interests',
            'Add Resource': '/upload-resource',
            Requests: '/requests',
            Chats: '/chats',
        };
    }

    return (
        <header className="flex flex-col gap-8 p-6 px-10 bg-gray-100">
            <div className='flex gap-20'>
                <Link to='/home' className="text-3xl italic font-bold">
                    NeighborShare
                </Link>
                <nav className='hidden lg:block'>
                    <ul className="flex flex-row gap-6">
                        {
                            navItems.map((navItem, idx) => {
                                const itemStyle = selected === navItem ? selectedStyle : navStyle;
                                return (
                                    <li key={idx.toString()}>
                                        <Link to={links[navItem]} className={itemStyle}>{navItem}</Link>
                                    </li>
                                );
                            })
                    }
                    </ul>
                </nav>
                <div className='ml-auto'>
                    <div className='flex gap-6'>
                        <div>
                            {
                                isAuthenticated
                                    ? (
                                        <div className="flex flex-col items-center justify-center ml-auto">
                                            { user.image
                                                ? <img className="h-12 w-12 rounded-full hover:cursor-pointer" src={user.image} alt="username" />
                                                : <div className="flex justify-center items-center text-lg bg-gray-300 font-bold h-12 w-12 rounded-full hover:cursor-pointer">
                                                    {user.username[0].toUpperCase()}
                                                  </div>
                                            }
                                            <div onClick={handleLogOut} className={linkStyle() + ' hover:cursor-pointer'} href="">sign out</div>
                                        </div>
                                    )
                                    : (
                                        <div className="flex gap-4">
                                            <Link to='/sign-in' className={buttonStyle() + ' px-8'}>sign in</Link>
                                            <Link to='/sign-up' className={buttonStyle() + ' px-8'}>sign up</Link>
                                        </div>
                                    )
                        }
                        </div>
                        <button onClick={handleNav}>
                            <Icon ref={button1Ref} className='lg:hidden' path={mdiMenu} size={2} />
                            <Icon ref={button2Ref} className='hidden lg:hidden' path={mdiClose} size={2} />
                        </button>
                    </div>
                </div>
            </div>
            <nav ref={navRef} className='hidden lg:hidden'>
                <ul className="flex flex-col gap-4">
                    {
                        navItems.map((navItem, idx) => {
                            const itemStyle = selected === navItem ? selectedStyle : navStyle;

                            return (
                                <li key={idx.toString()}>
                                    <Link to={links[navItem]} className={itemStyle}>{navItem}</Link>
                                </li>
                            );
                        })
                }
                </ul>
            </nav>
        </header>
    );
}

export function Search() {
    const [inputValue, setInputValue] = useState('');

    return (
        <div className="flex flex-row justify-center gap-4 mb-10">
            <input type="search" className="tracking-wider rounded-xl font-light p-3 w-1/3" placeholder="search for a resource"/>
            <button className={buttonStyle() + " px-8"}>search</button>
        </div>
    );
}

export function Modal({ isOpen, onClose, header, children }) {
    if (!isOpen) return null;

    return (
        <div className='flex justify-center items-center fixed inset-0 backdrop-blur-sm bg-opacity-50 bg-black'>
            <div className='bg-gray-200 rounded-2xl shadow-lg w-full max-w-md mx-4'>
                <div className='flex items-start p-2 border-b border-gray-100'>
                    <h2 className='text-center pl-2 pt-2 mr-auto font-semibold'>{header}</h2>
                    <button onClick={onClose} className='bg-green-600 hover:bg-green-400 rounded-xl text-white py-2 px-6 font-semibold'>ok</button>
                </div>
                <div className='px-8 pt-2 pb-8 text-center'>{children}</div>
            </div>
        </div>
    );
}

export function LoadingSpinner({ isOpen }) {
    if (!isOpen) return null;

    return (
      <div className='flex justify-center items-center fixed inset-0 bg-gray-100 cursor-wait'>
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-r-4 border-t-gray-500 border-r-gray-300"></div>
          </div>
      </div>
    );
}

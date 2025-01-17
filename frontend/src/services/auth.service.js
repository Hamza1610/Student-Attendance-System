import Cookies from 'js-cookie';

const saveGoogleUserToCookie = (googleUser) => {
    if (!googleUser || !googleUser.uid) {
        console.log('Invalid Google user object')
        throw new Error('Invalid Google user object');
    }

    const userId = googleUser.uid;
    Cookies.set('user_id', userId, { expires: 7 }); // Cookie expires in 7 days
};

const getUserIdFromCookie = () => {
    const userId = Cookies.get('user_id');
    if (userId) {
        console.log('User ID from cookie:', userId);
        return userId;
    } else {
        console.log('No user ID found in cookie');
        return null;
    }
};
export {saveGoogleUserToCookie, getUserIdFromCookie}
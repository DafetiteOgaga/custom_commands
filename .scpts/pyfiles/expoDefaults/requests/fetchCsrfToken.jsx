import AsyncStorage from '@react-native-async-storage/async-storage';
import { useState } from 'react';

function useGet () {
	const [getData, setGetData] = useState(null)
	const [isGetLoading, setIsGetLoading] = useState(false)
	const [isGetError, setIsGetError] = useState(null);
	const GetSetup = async (url) => {
		setIsGetLoading(true);
		setIsGetError(null);
		setGetData(null);
		try {
			const response = await fetch(url);
			if (!response.ok) {
				console.log('Failed to post data')
				setIsGetError('Failed to post data')
				throw new Error('Failed to post data')
			}
			const resp = await response.json()
			console.log('Response:', resp)
			console.log('Response success')
			setGetData(resp)
		} catch (e) {
			setIsGetError(`Error posting data (message): ${e.message}`);
			throw new Error('Error posting data (message):', e.message);
		} finally {
			setIsGetLoading(false);
		}
	}
	return {getData, isGetError, isGetLoading, GetSetup}
}
export { useGet };

function usePost () {
	const [postData, setPostData] = useState(null)
	const [isPostLoading, setIsPostLoading] = useState(false)
	const [isPostError, setIsPostError] = useState(null);
	const PostSetup = async (url, formData) => {
		const csrfToken = await fetchCsrfToken() // Fetch CSRF token
		setIsPostLoading(true);
		setIsPostError(null);
		setPostData(null);
		try {
			const response = await fetch(url,
				{
					method: 'POST',
					headers: {
						'X-CSRFToken': csrfToken,
					},
					credentials: 'include',
					body: formData,
				}
			);
			if (!response.ok) {
				console.log('Failed to post data')
				setIsPostError('Failed to post data')
				throw new Error('Failed to post data')
			}
			const resp = await response.json()
			console.log('Response:', resp)
			console.log('Response success')
			setPostData(resp)
		} catch (e) {
			setIsPostError(`Error posting data (message): ${e.message}`);
			throw new Error(`Error posting data (message): ${e.message}`);
		} finally {
			setIsPostLoading(false);
		}
	}
	return {postData, isPostError, isPostLoading, PostSetup}
}
export { usePost };

function usePut () {
	const [putData, setPutData] = useState(null)
	const [isPutLoading, setIsPutLoading] = useState(false)
	const [isPutError, setIsPutError] = useState(null);
	const PutSetup = async (url, formData) => {
		const csrfToken = await fetchCsrfToken() // Fetch CSRF token
		setIsPutLoading(true);
		setIsPutError(null);
		setPutData(null);
		try {
			const response = await fetch(url,
				{
					method: 'PUT',
					headers: {
						'X-CSRFToken': csrfToken,
					},
					credentials: 'include',
					body: formData,
				}
			);
			if (!response.ok) {
				console.log('Failed to post data')
				setIsPutError('Failed to post data')
				throw new Error('Failed to post data')
			}
			const resp = await response.json()
			console.log('Response:', resp)
			console.log('Response success')
			setPutData(resp)
		} catch (e) {
			setIsPutError(`Error posting data (message): ${e.message}`);
			throw new Error(`Error posting data (message): ${e.message}`);
		} finally {
			setIsPutLoading(false);
		}
	}
	return {putData, isPutError, isPutLoading, PutSetup}
}
export { usePut };

function usePatch () {
	const [patchData, setPatchData] = useState(null)
	const [isPatchLoading, setIsPatchLoading] = useState(false)
	const [isPatchError, setIsPatchError] = useState(null);
	const PatchSetup = async (url, formData) => {
		const csrfToken = await fetchCsrfToken() // Fetch CSRF token
		setIsPatchLoading(true);
		setIsPatchError(null);
		setPatchData(null);
		try {
			const response = await fetch(url,
				{
					method: 'PATCH',
					headers: {
						'X-CSRFToken': csrfToken,
					},
					credentials: 'include',
					body: formData,
				}
			);
			if (!response.ok) {
				console.log('Failed to post data')
				setIsPatchError('Failed to post data')
				throw new Error('Failed to post data')
			}
			const resp = await response.json()
			console.log('Response:', resp)
			console.log('Response success')
			setPatchData(resp)
		} catch (e) {
			setIsPatchError(`Error posting data (message): ${e.message}`);
			throw new Error(`Error posting data (message): ${e.message}`);
		} finally {
			setIsPatchLoading(false);
		}
	}
	return {patchData, isPatchError, isPatchLoading, PatchSetup}
}
export { usePatch };

function useDelete () {
	const [deleteData, setDeleteData] = useState(null)
	const [isDeleteLoading, setIsDeleteLoading] = useState(false)
	const [isDeleteError, setIsDeleteError] = useState(null);
	const DeleteSetup = async (url, formData) => {
		const csrfToken = await fetchCsrfToken() // Fetch CSRF token
		setIsDeleteLoading(true);
		setIsDeleteError(null);
		setDeleteData(null);
		try {
			const response = await fetch(url,
				{
					method: 'DELETE',
					headers: {
						'X-CSRFToken': csrfToken,
					},
					credentials: 'include',
					body: formData,
				}
			);
			if (!response.ok) {
				console.log('Failed to post data')
				setIsDeleteError('Failed to post data')
				throw new Error('Failed to post data')
			}
			const resp = await response.json()
			console.log('Response:', resp)
			console.log('Response success')
			setDeleteData(resp)
		} catch (e) {
			setIsDeleteError(`Error posting data (message): ${e.message}`);
			throw new Error(`Error posting data (message): ${e.message}`);
		} finally {
			setIsDeleteLoading(false);
		}
	}
	return {deleteData, isDeleteError, isDeleteLoading, DeleteSetup}
}
export { useDelete };

const fetchCsrfToken = async () => {
    console.log('Fetching CSRF token... ##### new');
    const response = await fetch('http://192.168.43.214:8000/api/get-csrf-token/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    });
    console.log('after fetching CSRF token:')
    if (!response.ok) {
        console.log('Failed to fetch CSRF token');
        return null;
    }
    console.log('Fetching CSRF token success')
    const data = await response.json();
    const csrfToken = data.csrfToken;

    // Save CSRF token to AsyncStorage
    await AsyncStorage.setItem('csrfToken', csrfToken);

    return csrfToken;
}
export { fetchCsrfToken };
import {useState, useEffect} from "react";
import { StyleSheet, Text, View, SafeAreaView, TextInput,
    Button, FlatList, ActivityIndicator, useColorScheme, Image,
    TouchableOpacity } from "react-native";

import { useCurrColorMode } from '@/constants/Colors';
import { StatusBar as MyBar } from 'expo-status-bar';
import { useNavigation } from 'expo-router';
import { ScreenStyle, generalstyles } from '../myConfig/navigation';
import { Ionicons } from '@expo/vector-icons';

import { usePost } from '../requests/fetchCsrfToken'
import Toast from 'react-native-toast-message';

interface postType {
    email: string,
    password: string,
}
interface notiType {
    type: string,
    msg: string
}

export default function Login() {
    const {postData, isPostError, isPostLoading, PostSetup} = usePost();
    const [secureText, setSecureText] = useState(true);
	const currColor = useCurrColorMode(); // get styles based on the current color mode
	const colorScheme = useColorScheme(); // Detect system theme
	const inputBgColor = colorScheme==='dark'?'#353939':'#b9b6b6'
	const placeholderTextColor = colorScheme==='dark'?'#777':'#bbb'
    const initials = {email: '', password: ''};
    const [loginPost, setLoginPost] = useState<postType>(initials)
    const [formData, setFormData] = useState(new FormData())
    const myDynamicStyles = StyleSheet.create({
        bgColor: {backgroundColor: currColor.background},
        textColor: {color: currColor.text},
        inputColor: {
            backgroundColor: currColor.background,
            borderColor: currColor.icon,
        },
        inputBgColor: {backgroundColor: inputBgColor}
    });
    const handleSubmit = () => {
        if (loginPost.email.trim()!=='' && loginPost.password.trim()!=='') {
            setFormData(new FormData());
            formData.append('email', loginPost.email);
            formData.append('password', loginPost.password);
            PostSetup(
                'http://192.168.43.214:8000/test-api/',
                formData
            );
        }
    }
    useEffect(()=>{
        if (postData) {
            console.log('Response login:', postData)
            setLoginPost(initials)
        } else if (isPostError) {
            console.log('Error:', isPostError)
        }
    }, [postData, isPostError])
    console.log(
        '\npostData:', postData,
        '\nerror:', isPostError,
        '\nloading:', isPostLoading
    )
    const showToast = (data: notiType) => {
        console.log('Toast:', data)
        Toast.show({
            type: data.type,  // 'success' | 'error' | 'info'
            text1: data.msg,
        });
    };
	return (
		<View style={[ScreenStyle.allScreenContainer, loginStyles.loginContainer]}>
			<View style={[generalstyles.formContainer,
				myDynamicStyles.bgColor
				]}>
				<Text // form/post container
				style={[generalstyles.headerFooter, myDynamicStyles.textColor, loginStyles.header]}>Login</Text>
                <View>
                    <TextInput // input1 (email/username)
                        style={[
                            generalstyles.input,
                            myDynamicStyles.inputColor,
                            myDynamicStyles.textColor,
                            myDynamicStyles.inputBgColor,
                            loginStyles.input,
                        ]}
                        placeholder="Email Address"
                        keyboardType="email-address"
                        placeholderTextColor={placeholderTextColor}
                        value={loginPost.email}
                        onChangeText={email=>setLoginPost({...loginPost, email})}
                    />
                </View>
                <View>
                    <TextInput // input2 (password)
                        style={[
                            generalstyles.input,
                            myDynamicStyles.inputColor,
                            myDynamicStyles.textColor,
                            myDynamicStyles.inputBgColor,
                            loginStyles.input,
                        ]}
                        placeholder="Password"
                        secureTextEntry={secureText}
                        placeholderTextColor={placeholderTextColor}
                        value={loginPost.password}
                        onChangeText={password=>setLoginPost({...loginPost, password})}
                    />
                    <TouchableOpacity
                    style={loginStyles.icon}
                    onPress={() => setSecureText(!secureText)}>
                        <Ionicons name={secureText ? "eye" : "eye-off"} size={24} color="gray" />
                    </TouchableOpacity>
                </View>
                {isPostLoading ? (<ActivityIndicator size="small" color="#f5f5f5" />):
				(<View style={loginStyles.button}>
                    <Button color={'#2A2A5F'} title={isPostLoading?'Login in ...':'Login'} onPress={handleSubmit}
                    disabled={isPostLoading}
                    />
                </View>)}
			</View>
            <View>
                <Button
                    title="Show Toast"
                    onPress={() => showToast({
                        type: 'success',
                        msg: 'This is a test message!'
                        })} />
            </View>
		</View>
	)
}

const loginStyles = StyleSheet.create({
    loginContainer: {
        justifyContent: 'center',
        alignSelf: 'center',
    },
    header: {
        marginHorizontal: 120,
    },
    input: {
        // height: 50,
        borderWidth: 1,
        borderColor: "gray",
        borderRadius: 8,
        paddingLeft: 15,
        paddingRight: 40, // Ensure space for the icon
        fontSize: 16,
    },
    icon: {
        position: "absolute",
        right: 10,
        top: "40%",
        transform: [{ translateY: -12 }],
    },
    button: {
        marginHorizontal: 100,
    }
})


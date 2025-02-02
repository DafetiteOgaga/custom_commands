import {useState, useEffect} from "react";
import { StyleSheet, Text, View, SafeAreaView, TextInput,
    Button, FlatList, ActivityIndicator, useColorScheme, Image, } from "react-native";

import { useCurrColorMode } from '@/constants/Colors';
import { StatusBar as MyBar } from 'expo-status-bar';
import { useNavigation } from 'expo-router';
import ScreenStyle from '@/hooks/ScreenStyle';

// type declarations
interface getType {
    userId: number,
    id: number,
    title: string,
    body: string,
}
interface postType {
    title: string,
    body: string,
}

// switch between images based on color scheme
const dafelogoDarkBg = require('@/assets/images/dafelogo1.png');
const dafelogoWhiteBg = require('@/assets/images/dafelogo4.png');

export default function App() {
    const navigation: any = useNavigation(); // navigation to set/update data to another screen/the screen itself
    const currColor = useCurrColorMode(); // get styles based on the current color mode
    const colorScheme = useColorScheme(); // Detect system theme
    const [isError, setIsError] = useState<string|null>(null);
    const initials = {title: '', body: ''};
    const [userPost, setUserPost] = useState<postType>(initials)
    const [posting, setIsPosting] = useState<boolean>(false)
    const [getData, setGetData] = useState<getType[]|null>(null);
    const [isLoading, setIsloading] = useState<boolean>(true);
    const [refreshing, setRefreshing] = useState<boolean>(false);
    const [limit, setLimit] = useState<number>(10);
    const dafelogo: any = colorScheme==='dark' ? dafelogoDarkBg : dafelogoWhiteBg;
    const placeholderTextColor = colorScheme==='dark'?'#777':'#bbb'
    const inputBgColor = colorScheme==='dark'?'#353939':'#b9b6b6'

    // Fetch data from API
    const fetchData = async () => {
        try {
            const response = await fetch(`https://jsonplaceholder.typicode.com/posts?_limit=${limit}`);
            if (!response.ok) {
                setIsError('Failed to fetch data')
                throw new Error('Failed to fetch data')
            }
            const data = await response.json();
            setIsError(null)
            setGetData(data);
        } catch (e: any) {
            setIsError(`Error fetching data (message): ${e.message}`)
            throw new Error('Error fetching data (message):', e.message);
        } finally {
            setIsloading(false)
        }
    }
    useEffect(()=>{fetchData()}, []) // Fetch data only on component mount
    const handleRefresh = () => { // Refresh/pull more data from server upon refresh
        setLimit(prev=>prev+10);
        setRefreshing(true);
        fetchData();
        setRefreshing(false);
    }

    // Post data to API
    const handleSubmit = async () => {
        setIsPosting(true);
        try {
            const response = await fetch('https://jsonplaceholder.typicode.com/posts',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(userPost),
                }
            );
            if (!response.ok) {
                setIsError('Failed to post data')
                throw new Error('Failed to post data')
            }
            const resp = await response.json()
            setIsError(null)
            setGetData(getData?[resp, ...getData]:[resp]);
            setUserPost(initials)
        } catch (e: any) {
            setIsError(`Error posting data (message): ${e.message}`);
            throw new Error('Error posting data (message):', e.message);
        } finally {
            setIsPosting(false);
        }
    }

    // Dynamic styles based on color scheme
    const myDynamicStyles = StyleSheet.create({
        bgColor: {backgroundColor: currColor.background},
        textColor: {color: currColor.text},
        inputColor: {
            backgroundColor: currColor.background,
            borderColor: currColor.icon,
        },
        inputBgColor: {backgroundColor: inputBgColor}
    });

    // Loading screen (if data is still loading)
    if (isLoading) {
        return (
            <SafeAreaView style={[ScreenStyle.allScreenContainer, styles.loading]}>
                <MyBar style="auto" />
                <ActivityIndicator size="large" color="blue" />
                <Text style={[myDynamicStyles.textColor]}>Loading...</Text>
            </SafeAreaView>
        )
    }

    return (
        <>
            {/* safeareaview works only on ios */}
            <SafeAreaView style={[ScreenStyle.allScreenContainer]}>
            <MyBar // StatusBar styling
            style="auto" />

            <View style={styles.imageContainer}>
                <Image // logo
                source={dafelogo} style={styles.image} />
            </View>

            {isError? // if there's an error, show error message
                (<View style={styles.errorContainer}>
                    <Text style={styles.errorText}>Oopsy!</Text>
                    <Text style={styles.errorText}>{isError}</Text>
                </View>) :
                (// otherwise, if there's no error, show the form and the data
                <>

                <View style={[styles.formContainer, myDynamicStyles.bgColor]}>
                    <Text // form/post container
                    style={[styles.headerFooter, myDynamicStyles.textColor]}>Create Post</Text>
                    <TextInput // input1 (title)
                        style={[styles.input, myDynamicStyles.inputColor, myDynamicStyles.textColor, myDynamicStyles.inputBgColor]}
                        placeholder="Title"
                        placeholderTextColor={placeholderTextColor}
                        value={userPost.title}
                        onChangeText={title=>setUserPost({...userPost, title})}
                    />
                    <TextInput // input2 (body)
                        style={[styles.input, myDynamicStyles.inputColor, myDynamicStyles.textColor, myDynamicStyles.inputBgColor]}
                        placeholder="Body"
                        placeholderTextColor={placeholderTextColor}
                        value={userPost.body}
                        onChangeText={body=>setUserPost({...userPost, body})}
                    />
                    <Button title={posting?'Posting...':'Post'} onPress={handleSubmit}
                    disabled={posting}
                    />
                </View>

                <View style={{paddingHorizontal: 90, paddingBottom: 20}}>
                    <Button // button to go to Greet screen with data passed from this screen to Greet screen
                    title="Goto Greet" onPress={()=>navigation.navigate("greet", {
                        message: "Hello from Index!\nShit be working!",
                        myName: "Dafe"
                        })} />
                </View>

                {getData && //data container
                <View>
                    <FlatList // preferred way to display data over map()
                    data={getData}
                    renderItem={({item})=>{
                        return (
                            <View style={[styles.card, myDynamicStyles.bgColor]}>
                                <Text style={[styles.titleText, myDynamicStyles.textColor]}>{item.title}</Text>
                                <Text style={[myDynamicStyles.textColor]}>{item.body}</Text>
                            </View>
                    )}}
                    keyExtractor={(item, index)=>item.id+index+item.title.toString()}
                    ItemSeparatorComponent={()=><View style={{height: 5}} />}
                    ListEmptyComponent={()=><Text style={[styles.notFound, myDynamicStyles.textColor]}>No Post found</Text>}
                    ListHeaderComponent={()=><Text style={[styles.headerFooter, myDynamicStyles.textColor]}>Post List {getData.length} Items</Text>}
                    ListFooterComponent={()=><Text style={[styles.headerFooter, myDynamicStyles.textColor, {paddingBottom: 320,}]}>End of Post</Text>}
                    refreshing={refreshing}
                    onRefresh={handleRefresh}
                    />
                </View>}</>)}
            </SafeAreaView>
        </>
    )
}

const styles = StyleSheet.create({
    card: {
        padding: 16,
        borderRadius: 10,
        borderWidth: 1,
    },
    titleText: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    notFound: {
        fontSize: 20,
        fontWeight: 'bold',
        alignSelf: 'center',
        paddingTop: 100
    },
    headerFooter: {
        fontSize: 25,
        fontWeight: 'bold',
        alignSelf: 'center',
        padding: 10,
    },
    loading: {
        justifyContent: 'center',
        alignItems: 'center',
    },
    formContainer: {
        padding: 20,
        borderRadius: 10,
        marginBottom: 10,
        borderWidth: 1,
    },
    input: {
        borderWidth: 1,
        padding: 10,
        marginBottom: 10,
        borderRadius: 5,
    },
    errorContainer: {
        paddingTop: 100,
    },
    errorText: {
        fontSize: 25,
        fontWeight: 'bold',
        alignSelf: 'center',
        color: 'red',
        textAlign: 'center',
        // borderWidth: 1,
        paddingTop: 10,
    },
    imageContainer: {
        // width: 10
    },
    image: {
        width: 100,
        height: 40,
        resizeMode: 'contain',
    },
});

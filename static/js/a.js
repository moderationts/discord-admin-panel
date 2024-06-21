findByProps("addInterceptor").addInterceptor(e=>{
    if (e.type === "USER_PROFILE_FETCH_SUCCESS" && e.user.id === "YOUR USER ID HERE"){
        e.guild_member_profile.profile_effect = {
            id:"profile effect id here" // get it from collectibles.happyenderman.com 
        }
    }
})
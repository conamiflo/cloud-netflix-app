import {Injectable} from '@angular/core';
import {UserDTO} from "../../models/UserDTO";
import {Router} from "@angular/router";
import {Amplify, Auth} from 'aws-amplify';
// @ts-ignore
import awsconfigure from '../../../../aws-exports.js'
import {BehaviorSubject} from "rxjs";

Amplify.configure(awsconfigure)

//@angularJitApplicationTransform(mod16)

@Injectable({
  providedIn: 'root'
})
export class CognitoService {
  private authenticationSubject: BehaviorSubject<any>;

  constructor(private router: Router,) {
    this.authenticationSubject = new BehaviorSubject<boolean>(false);
  }

  public async signIn(username: string, password: string) {
    try {
      var l=await Auth.signIn(username, password)
      console.log(l)
      return true
    } catch (e) {
      console.log('Auth error',e )
      return false
      // Outputs: Auth error The user is not authenticated
    }
  }

  public async getUser(): Promise<any| undefined> {
    try {
      const userInfo = await Auth.currentUserInfo();
      return userInfo;
    } catch (error) {
      return null; // or handle the error as appropriate for your application
    }
  }

  async getUsername(): Promise<string | null> {
    try {
      const userInfo = await Auth.currentUserInfo();
      if (userInfo && userInfo.username) {
        return userInfo.username;
      } else {
        return null;
      }
    } catch (error) {
      console.error('Error getting user info:', error);
      return null;
    }
  }

  public async signOut(): Promise<any> {
    await Auth.signOut()

  }

  async getJWT(){
    var res=await Auth.currentSession()
    var jwt=res.getAccessToken().decodePayload()

    return jwt;
  }

  async getUserGroup():Promise<string[]|null> {
    try {
      var res=await Auth.currentSession()
      console.log(res)
      var jwt=res.getAccessToken().decodePayload()
      var groups=jwt['cognito:groups'];
     if(groups==undefined) return [];
     return groups;
    }catch (e){
      return null
    }

  }

  async confirmSignUp(username:string,code:string):Promise<boolean> {
    try {
      await Auth.confirmSignUp(username,code)
      return true
    }catch (e){
      return false
    }

  }





  async signUp(usr:UserDTO) {
    var username=usr.username
    var password=usr.password
    var phone_number=usr.phone_number
    var email=usr.email
    var given_name=usr.name
    var family_name=usr.family_name
    try {
      const { user } = await Auth.signUp({
        username,
        password,
        attributes: {
          email, // optional
          phone_number, // optional - E.164 number convention
          given_name,// other custom attributes
          family_name
        },
        autoSignIn: {
          // optional - enables auto sign in after user is confirmed
          enabled: false
        }
      });
      console.log(user);
      return '';
    } catch (error) {
      console.log('error signing up:', error);
      return error as string;
    }
  }
}

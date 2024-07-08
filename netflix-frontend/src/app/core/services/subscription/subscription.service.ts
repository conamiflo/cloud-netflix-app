import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import { Observable} from "rxjs";
import {environment} from "../../../../env/env";
import {CognitoService} from "../cognito/cognito.service";

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  constructor(private httpClient: HttpClient,private cognitoService:CognitoService) {}

  async subscribe(username: string, type: string, value: string): Promise<Observable<any>> {
    var valueJwt = await this.cognitoService.getJWT()
    const url = environment.cloudHost + 'subscriptions';
    const headers = new HttpHeaders()
    .append('authorizationtoken', valueJwt as string)
    .append('Content-Type', 'application/json')

    const body = {username, type, value};
    return this.httpClient.post<any>(url, body, {headers});
  }

  async getSubscriptions(username: string): Promise<Observable<any>> {
    let params = new HttpParams()
      .set('username', username);
    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationtoken', value as string);

    return this.httpClient.get(environment.cloudHost + 'subscriptions', {headers,params});
  }

  async unsubscribe(username: string, subscriptionId: string): Promise<Observable<any>> {
    const url = environment.cloudHost + 'subscriptions';
    var value = await this.cognitoService.getJWT()
    const headers = new HttpHeaders()
      .append('authorizationtoken', value as string);
    const params = new HttpParams()
      .set('subscription_id', subscriptionId)
      .set('username', username);
    return this.httpClient.delete(url, {headers,params});
  }

}

import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {map, Observable} from "rxjs";
import {environment} from "../../../../env/env";

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  constructor(private httpClient: HttpClient) {}

  subscribe(username: string, type: string, value: string): Observable<any> {
    const url = environment.cloudHost + 'subscriptions';
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    const body = { username, type, value };
    return this.httpClient.post<any>(url, body, { headers });
  }

  getSubscriptions(username: string): Observable<any> {
    let params = new HttpParams()
      .set('username', username);

    return this.httpClient.get(environment.cloudHost + 'subscriptions', { params });
  }

  unsubscribe(username: string, subscriptionId: string): Observable<any> {
    const url = environment.cloudHost + 'subscriptions';
    const params = new HttpParams()
      .set('subscription_id', subscriptionId)
      .set('username', username);
    return this.httpClient.delete(url, { params });
  }

}

import { Component } from '@angular/core';
import {SubscriptionsCardComponent} from "../subscriptions-card/subscriptions-card.component";

@Component({
  selector: 'app-subscriptions',
  standalone: true,
  imports: [
    SubscriptionsCardComponent
  ],
  templateUrl: './subscriptions.component.html',
  styleUrl: './subscriptions.component.css'
})
export class SubscriptionsComponent {

}

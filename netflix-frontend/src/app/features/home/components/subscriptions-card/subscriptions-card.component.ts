import { Component } from '@angular/core';
import {IonIcon} from "@ionic/angular/standalone";
import {NgForOf} from "@angular/common";
import {addIcons} from "ionicons";
import {send, star} from "ionicons/icons";

@Component({
  selector: 'app-subscriptions-card',
  standalone: true,
    imports: [
        IonIcon,
        NgForOf
    ],
  templateUrl: './subscriptions-card.component.html',
  styleUrl: './subscriptions-card.component.css'
})
export class SubscriptionsCardComponent {
  constructor() {
    addIcons({star,send});
  }
}

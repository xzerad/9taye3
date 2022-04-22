import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent implements OnInit {
  @Input() imageUrl: string | undefined
  @Input() title: string | undefined
  @Input() brand: string | undefined
  @Input() description: string | undefined
  @Input() location: string | undefined
  @Input() site: string | undefined
  @Input() price: string | undefined


  constructor() { }

  ngOnInit(): void {
  }

}

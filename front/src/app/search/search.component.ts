import {Component, Input, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent {
  constructor(private http: HttpClient) {
  }
  found=false;
  total = 0;
  size = 10
  search = new Search();
  category = [
    {
   option: "Peripheriques et Accessoires",
   slug: "peripheriques-accessoires"
  },
    {
      option: "Composants et Stockage",
      slug: "composants-stockage"
    },
    {
      option: "pc",
      slug: "pc"
    }
  ]
  selectedCategory: string = ""
  products: any
  private request(url: string){
    this.http.get(
      url
    ).subscribe(
      (data: any)=> this.process(data)
    )
  }
  public showProducts(){
    if(this.selectedCategory){
      this.request(`http://127.0.0.1:8000/?q=${this.search.value}&cat=${this.selectedCategory}`)
    }else{
      console.log(this.selectedCategory)
      this.request(`http://127.0.0.1:8000/?q=${this.search.value}`)
    }
  }
  click(e: any){
    let skip = 10 * e.pageIndex;
    console.log(e);
    if(this.selectedCategory){
      this.request(`http://127.0.0.1:8000/?q=${this.search.value}&cat=${this.selectedCategory}&skip=${skip}`)
    }else{
      console.log(this.selectedCategory)
      this.request(`http://127.0.0.1:8000/?q=${this.search.value}&skip=${skip}`)
    }
  }
  private process(data: any){
    this.products = data?.hits.hits;
    this.size = this.products.length ;
    this.total = data?.hits? Math.ceil(data.hits.total.value/this.size): 1

    this.found = this.size > 0;
    console.log(this.size)

  }

}
export class Search{
  value: any = "";
  setValue(val: any){
      this.value = val;
  }

}

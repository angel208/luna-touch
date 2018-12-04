import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TtsConfigComponent } from './tts-config.component';

describe('TtsConfigComponent', () => {
  let component: TtsConfigComponent;
  let fixture: ComponentFixture<TtsConfigComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TtsConfigComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TtsConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

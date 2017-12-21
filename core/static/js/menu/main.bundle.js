webpackJsonp(["main"],{

/***/ "../../../../../src/$$_lazy_route_resource lazy recursive":
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncatched exception popping up in devtools
	return Promise.resolve().then(function() {
		throw new Error("Cannot find module '" + req + "'.");
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "../../../../../src/$$_lazy_route_resource lazy recursive";

/***/ }),

/***/ "../../../../../src/app/app-routing.module.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppRoutingModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_router__ = __webpack_require__("../../../router/esm5/router.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__quiz_quiz_component__ = __webpack_require__("../../../../../src/app/quiz/quiz.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_common__ = __webpack_require__("../../../common/esm5/common.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




var routes = [
    { path: '', component: __WEBPACK_IMPORTED_MODULE_2__quiz_quiz_component__["a" /* QuizComponent */] },
    { path: 'review', component: __WEBPACK_IMPORTED_MODULE_2__quiz_quiz_component__["a" /* QuizComponent */] },
    { path: 'submit', component: __WEBPACK_IMPORTED_MODULE_2__quiz_quiz_component__["a" /* QuizComponent */] },
];
var AppRoutingModule = (function () {
    function AppRoutingModule() {
    }
    AppRoutingModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["I" /* NgModule */])({
            imports: [__WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* RouterModule */].forRoot(routes)],
            exports: [__WEBPACK_IMPORTED_MODULE_1__angular_router__["a" /* RouterModule */]],
            providers: [{ provide: __WEBPACK_IMPORTED_MODULE_3__angular_common__["a" /* APP_BASE_HREF */], useValue: '/menu/test' }]
        })
    ], AppRoutingModule);
    return AppRoutingModule;
}());



/***/ }),

/***/ "../../../../../src/app/app.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "/* AppComponent's private CSS styles */\nh1 {\n  font-size: 1.2em;\n  color: #999;\n  margin-bottom: 0;\n}\nh2 {\n  font-size: 2em;\n  margin-top: 0;\n  padding-top: 0;\n}\nnav a {\n  padding: 5px 10px;\n  text-decoration: none;\n  margin-top: 10px;\n  display: inline-block;\n  background-color: #eee;\n  border-radius: 4px;\n}\nnav a:visited, a:link {\n  color: #607D8B;\n}\nnav a:hover {\n  color: #039be5;\n  background-color: #CFD8DC;\n}\nnav a.active {\n  color: #039be5;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/app.component.html":
/***/ (function(module, exports) {

module.exports = "<router-outlet></router-outlet>\n\n"

/***/ }),

/***/ "../../../../../src/app/app.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};

var AppComponent = (function () {
    function AppComponent() {
    }
    AppComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-root',
            template: __webpack_require__("../../../../../src/app/app.component.html"),
            styles: [__webpack_require__("../../../../../src/app/app.component.css")]
        })
    ], AppComponent);
    return AppComponent;
}());



/***/ }),

/***/ "../../../../../src/app/app.module.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__ = __webpack_require__("../../../platform-browser/esm5/platform-browser.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__app_component__ = __webpack_require__("../../../../../src/app/app.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__quiz_quiz_component__ = __webpack_require__("../../../../../src/app/quiz/quiz.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__app_routing_module__ = __webpack_require__("../../../../../src/app/app-routing.module.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__quiz_service__ = __webpack_require__("../../../../../src/app/quiz.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__in_memory_data_service__ = __webpack_require__("../../../../../src/app/in-memory-data.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__angular_forms__ = __webpack_require__("../../../forms/esm5/forms.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__quiz_review_quiz_review_component__ = __webpack_require__("../../../../../src/app/quiz-review/quiz-review.component.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};










var AppModule = (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["I" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_2__app_component__["a" /* AppComponent */],
                __WEBPACK_IMPORTED_MODULE_3__quiz_quiz_component__["a" /* QuizComponent */],
                __WEBPACK_IMPORTED_MODULE_9__quiz_review_quiz_review_component__["a" /* QuizReviewComponent */]
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__["a" /* BrowserModule */],
                __WEBPACK_IMPORTED_MODULE_8__angular_forms__["a" /* FormsModule */],
                __WEBPACK_IMPORTED_MODULE_4__app_routing_module__["a" /* AppRoutingModule */],
                __WEBPACK_IMPORTED_MODULE_6__angular_common_http__["b" /* HttpClientModule */],
            ],
            providers: [__WEBPACK_IMPORTED_MODULE_5__quiz_service__["a" /* QuizService */], __WEBPACK_IMPORTED_MODULE_7__in_memory_data_service__["a" /* InMemoryDataService */]],
            bootstrap: [__WEBPACK_IMPORTED_MODULE_2__app_component__["a" /* AppComponent */]]
        })
    ], AppModule);
    return AppModule;
}());



/***/ }),

/***/ "../../../../../src/app/in-memory-data.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return InMemoryDataService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};

var InMemoryDataService = (function () {
    function InMemoryDataService() {
    }
    InMemoryDataService.prototype.createDb = function () {
        var test = [
            { id: 'get_quiz', time_to_pass: 15, score_to_pass: 60, name: 'Waiters test', questions: this.createQuestions(10) },
        ];
        return { test: test };
    };
    InMemoryDataService.prototype.createQuestions = function (num) {
        var questions = [];
        var drinks = { 0: 'Rum', 1: 'Tapioca', 2: 'Whiskey', 3: 'Vodka' };
        for (var i = 0; i < num; i++) {
            questions.push({ id: i, name: 'What is the best ' + drinks[i % 4],
                answers: this.createAnswers(i), answered: true });
        }
        return questions;
    };
    InMemoryDataService.prototype.createAnswers = function (num) {
        var answers = [];
        for (var i = 0; i < 4; i++) {
            answers.push({ id: 1, questionId: 1, isAnswer: i == 1,
                name: 'koko_' + (num + 1) + '_' + (i + 1), selected: false });
        }
        return answers;
    };
    InMemoryDataService = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* Injectable */])()
    ], InMemoryDataService);
    return InMemoryDataService;
}());



/***/ }),

/***/ "../../../../../src/app/models/answer.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Answer; });
var Answer = (function () {
    function Answer(data) {
        data = data || {};
        this.id = data.id;
        this.questionId = data.question;
        this.name = data.content;
        this.isAnswer = data.is_correct;
    }
    return Answer;
}());



/***/ }),

/***/ "../../../../../src/app/models/question.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Question; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__answer__ = __webpack_require__("../../../../../src/app/models/answer.ts");

var Question = (function () {
    function Question(data) {
        var _this = this;
        data = data || {};
        this.id = data.id;
        this.name = data.content;
        this.answers = [];
        data.answers.forEach(function (a) {
            _this.answers.push(new __WEBPACK_IMPORTED_MODULE_0__answer__["a" /* Answer */](a));
        });
    }
    return Question;
}());



/***/ }),

/***/ "../../../../../src/app/models/quiz.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return Quiz; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__question__ = __webpack_require__("../../../../../src/app/models/question.ts");

var Quiz = (function () {
    function Quiz(data) {
        var _this = this;
        if (data) {
            this.id = data.id;
            this.name = data.name;
            this.scoreToPass = data.score_to_pass;
            this.time = data.time_to_pass;
            this.questions = [];
            if (data.questions) {
                data.questions.forEach(function (q) {
                    _this.questions.push(new __WEBPACK_IMPORTED_MODULE_0__question__["a" /* Question */](q));
                });
            }
            else {
                this.questions = [];
            }
        }
    }
    return Quiz;
}());



/***/ }),

/***/ "../../../../../src/app/quiz-review/quiz-review.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".answered {\n  background-color:lightskyblue;\n  border:1px solid lightskyblue;\n  margin:2px 0;\n  padding:12px;\n}\n\n.not-answered {\n  background-color:#ffcccc;\n  border:1px solid #eeaaaa;\n  margin:2px 0;\n  padding:12px;\n}\n\n.offset-sm-4 {\n  margin-bottom: 40px;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/quiz-review/quiz-review.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"container\">\n  <div class=\"row\">\n    <div class=\"col-sm-4\" *ngFor=\"let question of quiz.questions; let index = index;\">\n      <div [ngClass]=\"{'answered': isAnswered(question), 'not-answered': !isAnswered(question)}\"\n           (click)=\"gotoQuestion(question.id)\">\n        {{index + 1}}. <strong>{{ question.name }}</strong> <hr>\n        Your answer: <i>{{ selectedAnswer(question) }}</i>\n      </div>\n    </div>\n  </div>\n  <div class=\"row\">\n    <div class=\"col-sm-4 offset-sm-4\">\n      <button class=\"btn btn-lg btn-primary\">Submit</button> <br>\n        <small>Click on a question to view it</small>\n    </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/quiz-review/quiz-review.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuizReviewComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__models_quiz__ = __webpack_require__("../../../../../src/app/models/quiz.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var QuizReviewComponent = (function () {
    function QuizReviewComponent() {
        this.showQuestion = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["v" /* EventEmitter */]();
    }
    QuizReviewComponent.prototype.ngOnInit = function () {
        console.log(JSON.stringify(this.quiz.questions[0].answers[0]));
    };
    QuizReviewComponent.prototype.isAnswered = function (question) {
        return !!question.answers.find(function (x) { return x.selected; });
    };
    ;
    QuizReviewComponent.prototype.selectedAnswer = function (question) {
        var name;
        question.answers.forEach(function (a) {
            console.log('selected: ' + a.selected);
            if (a.selected) {
                name = a.name;
            }
        });
        return name ? name : "not answered";
    };
    QuizReviewComponent.prototype.gotoQuestion = function (questionId) {
        console.log(questionId);
        this.showQuestion.emit(questionId);
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["D" /* Input */])(),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_1__models_quiz__["a" /* Quiz */])
    ], QuizReviewComponent.prototype, "quiz", void 0);
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["P" /* Output */])(),
        __metadata("design:type", __WEBPACK_IMPORTED_MODULE_0__angular_core__["v" /* EventEmitter */])
    ], QuizReviewComponent.prototype, "showQuestion", void 0);
    QuizReviewComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-quiz-review',
            template: __webpack_require__("../../../../../src/app/quiz-review/quiz-review.component.html"),
            styles: [__webpack_require__("../../../../../src/app/quiz-review/quiz-review.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], QuizReviewComponent);
    return QuizReviewComponent;
}());



/***/ }),

/***/ "../../../../../src/app/quiz.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuizService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var QuizService = (function () {
    function QuizService(http) {
        this.http = http;
        this.menuUrl = 'menu/test'; // URL to web api
    }
    /** GET Quiz */
    QuizService.prototype.getQuiz = function () {
        return this.http.get(this.menuUrl + '/get_quiz');
    };
    /** GET Questions */
    QuizService.prototype.getQuestions = function () {
        return this.http.get(this.menuUrl + '/questions');
    };
    QuizService = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["A" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */]])
    ], QuizService);
    return QuizService;
}());



/***/ }),

/***/ "../../../../../src/app/quiz/quiz.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".jumbotron {\n  text-align: center;\n}\n\na:hover {\n  color:#607D8B;\n}\n\n.badge {\n  display: inline-block;\n  font-size: small;\n  color: white;\n  padding: 0.8em 0.7em 0 0.7em;\n  background-color: #607D8B;\n  line-height: 1em;\n  position: relative;\n  left: -1px;\n  top: -4px;\n  height: 1.8em;\n  min-width: 16px;\n  text-align: right;\n  margin-right: .8em;\n  border-radius: 4px 0 0 4px;\n}\n\n.button {\n  background-color: #eee;\n  border: none;\n  padding: 5px 10px;\n  border-radius: 4px;\n  cursor: pointer;\n  cursor: hand;\n  font-family: Arial;\n}\n\nbutton:hover {\n  background-color: #cfd8dc;\n}\n\nbutton.delete {\n  position: relative;\n  left: 194px;\n  top: -32px;\n  background-color: gray !important;\n  color: white;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/quiz/quiz.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"jumbotron\" *ngIf=\"quiz\">\n  <h2>{{quiz.name}}</h2>\n  <p >You'll have {{quiz.time}} minutes to solve it, minimum score is {{quiz.scoreToPass}}, Good luck</p>\n  <a href=\"/\" class=\"btn btn-primary\">Back to dashboard</a>\n</div>\n<div class=\"container\" *ngIf=\"mode == 'quiz' && quiz\">\n  <div class=\"badge badge-info\">Question {{currIndex + 1}} of {{quiz.questions.length}}.</div>\n  <h2>{{currIndex + 1}}. <span [innerHTML]=\"getCurrQuestion().name\"></span></h2>\n  <div class=\"row\">\n    <div class=\"col-md-6\" *ngFor=\"let answer of getCurrQuestion().answers\">\n      <div class=\"option\">\n        <label class=\"\" [attr.for]=\"answer.id\">\n          <input id=\"{{answer.id}}\" type=\"checkbox\" [(ngModel)]=\"answer.selected\"/>\n          {{answer.name}}\n        </label>\n      </div>\n    </div>\n  </div>\n  <hr>\n  <div class=\"text-sm-center\">\n    <button class=\"btn btn-default\" (click)=\"goTo(0);\">First</button>\n    <button class=\"btn btn-info\" (click)=\"goTo(currIndex - 1);\">Prev</button>\n    <button class=\"btn btn-primary\" (click)=\"goTo(currIndex + 1);\">Next</button>\n    <button class=\"btn btn-default\" (click)=\"goTo(count - 1);\">Last</button>\n  </div>\n  <div class=\"text-sm-center\">\n    <button class=\"btn btn-success\" (click)=\"mode = 'review'\" style=\"margin-top: 20px\">Review and submit</button>\n  </div>\n</div>\n\n<app-quiz-review [quiz]=\"quiz\" (showQuestion)=\"showQuestion($event)\"\n                 *ngIf=\"mode == 'review' && quiz\"></app-quiz-review>\n"

/***/ }),

/***/ "../../../../../src/app/quiz/quiz.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return QuizComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__models_quiz__ = __webpack_require__("../../../../../src/app/models/quiz.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__quiz_service__ = __webpack_require__("../../../../../src/app/quiz.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var QuizComponent = (function () {
    function QuizComponent(quizService) {
        this.quizService = quizService;
        this.currIndex = 0;
        this.mode = 'quiz';
    }
    QuizComponent.prototype.ngOnInit = function () {
        this.loadQuiz();
    };
    QuizComponent.prototype.loadQuiz = function () {
        var _this = this;
        this.quizService.getQuiz().subscribe(function (res) {
            console.log(JSON.stringify(res));
            _this.quiz = new __WEBPACK_IMPORTED_MODULE_1__models_quiz__["a" /* Quiz */](res);
            console.log(JSON.stringify(_this.quiz));
            _this.count = _this.quiz.questions.length;
        }, function (err) {
            console.error("Error: " + err.message);
        });
    };
    QuizComponent.prototype.getCurrQuestion = function () {
        return this.quiz.questions[this.currIndex];
    };
    QuizComponent.prototype.goTo = function (index) {
        if (index >= 0 && index < this.count) {
            this.currIndex = index;
        }
    };
    QuizComponent.prototype.showQuestion = function (id) {
        this.mode = 'quiz';
        this.goTo(id);
    };
    QuizComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
            selector: 'app-quiz',
            template: __webpack_require__("../../../../../src/app/quiz/quiz.component.html"),
            styles: [__webpack_require__("../../../../../src/app/quiz/quiz.component.css")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_2__quiz_service__["a" /* QuizService */]])
    ], QuizComponent);
    return QuizComponent;
}());



/***/ }),

/***/ "../../../../../src/environments/environment.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return environment; });
// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.
var environment = {
    production: false
};


/***/ }),

/***/ "../../../../../src/main.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__ = __webpack_require__("../../../platform-browser-dynamic/esm5/platform-browser-dynamic.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__app_app_module__ = __webpack_require__("../../../../../src/app/app.module.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");




if (__WEBPACK_IMPORTED_MODULE_3__environments_environment__["a" /* environment */].production) {
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_13" /* enableProdMode */])();
}
Object(__WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__["a" /* platformBrowserDynamic */])().bootstrapModule(__WEBPACK_IMPORTED_MODULE_2__app_app_module__["a" /* AppModule */])
    .catch(function (err) { return console.log(err); });


/***/ }),

/***/ 0:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("../../../../../src/main.ts");


/***/ })

},[0]);
//# sourceMappingURL=main.bundle.js.map
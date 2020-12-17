<template>
  <div>
    <b-container>
      <b-row>
        <b-col cols="2"></b-col>
        <b-col cols="8" align="center">
          <b-card class="mb-2 mt-2">
            <div id="significance">
              <label for="significance">Уровень значимости</label>
              <b-form-select id="significance" v-model.number="significance" type="number">
                <option>0.01</option>
                <option>0.05</option>
              </b-form-select>
              <b-button @click="send_significance" variant="primary" class="mt-4" id="send_sign">Сохранить</b-button>
            </div>
            <div id="param_1" style="display: none">
              <label for="param_1">Наблюдаемое значение критерия Стьюдента для {{ params[0] }}:</label>
              <b-form-input v-model.number="param_1" type="number" />
              <b-button @click="display_param_2" variant="primary" class="mt-4" id="param_1_btn">Сохранить</b-button>
            </div>
            <div id="param_2" style="display: none">
              <label for="param_2">Наблюдаемое значение критерия Стьюдента для {{ params[1] }}:</label>
              <b-form-input v-model.number="param_2" type="number" />
              <b-button @click="send_params" variant="primary" class="mt-4" id="param_2_btn">Сохранить</b-button>
            </div>
            <div id="crit_values" style="display: none">
              <b-row>
                <b-col cols="6">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Число степеней свободы</th>
                    <th>Критическое значение</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(n, i) in vals.length" v-if="i<13" :key="i">
                    <td>{{ df[i] }}</td>
                    <td>{{ vals[i] }}</td>
                  </tr>
                </tbody>
              </table>
              </b-col>
              <b-col cols="6">
                <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Число степеней свободы</th>
                    <th>Критическое значение</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(n, j) in vals.length" v-if="j>=13" :key="j">
                    <td>{{ df[j] }}</td>
                    <td>{{ vals[j] }}</td>
                  </tr>
                </tbody>
              </table>
              </b-col>
              </b-row>
              <label for="param_1">Введите число степеней свободы критерия Стьюдента:</label>
              <b-form-input v-model.number="check_df" type="number" />
              <b-button @click="send_check_df" variant="primary" class="mt-4" id="check_df_btn">Сохранить</b-button>
            </div>
            <div id="sign_1" style="display: none">
              <p>Наблюдаемое значение критерия: {{ prac_values[params_index[0]] }}</p>
              <p>Критическое значение критерия: {{ crit_value }}</p>
              <p>Оценка параметра {{ params[0] }} значима?</p>
              <b-button @click="is_sign(true, params_index[0])" variant="primary">Да</b-button>
              <b-button @click="is_sign(false, params_index[0])" variant="primary">Нет</b-button>
            </div>
            <div id="sign_2" style="display: none">
              <p>Наблюдаемое значение критерия: {{ prac_values[params_index[1]] ? Number(prac_values[params_index[1]].toFixed(2)): prac_values[params_index[1]] }}</p>
              <p>Критическое значение критерия: {{ crit_value }}</p>
              <p>Оценка параметра {{ params[1] }} значима?</p>
              <b-button @click="is_sign(true, params_index[1])" variant="primary">Да</b-button>
              <b-button @click="is_sign(false, params_index[1])" variant="primary">Нет</b-button>
            </div>
            <div id="sign_table" style="display: none">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Обозначение</th>
                    <th>Оценка</th>
                    <th>Критерий</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(n, i) in params_list.length" :key="i">
                    <td>{{ params_list[i] }}</td>
                    <td>{{ param_values[i] ? Number(param_values[i].toFixed(2)): param_values[i] }}</td>
                    <td>{{ prac_values[i] ? Number(prac_values[i].toFixed(2)) : prac_values }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </b-card>
          <b-alert class="mt-2" variant="danger" :show="significance_answer ? true : false">
            {{ significance_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="param_answer ? true : false">
            {{ param_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="df_answer ? true : false">
            {{ df_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="info" :show="sign_answer ? true : false">
            {{ sign_answer }}</b-alert
          >
          <b-alert class="mt-2" variant="danger" :show="sign_wrong ? true : false">
            {{ sign_wrong }}</b-alert
          >
        </b-col>
      </b-row>
    </b-container>
    <div class="documentation">
      <b-card bg-variant="info">
        <p>
          Наблюдаемое значение критерия Стьюдента - статистика, вычисленная для указанного
          параметра как отношение модуля оценки к ее среднеквадратическому отклонению,
          вычисленному по дисперсии параметра модели.
        </p>
        <p>Например, если получена дисперсия оценок параметров модели:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Обозначение</th>
                  <th>Оценка</th>
                  <th>Дисперсия</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>B0</td>
                  <td>-0.891</td>
                  <td>0.032</td>
                </tr>
                <tr>
                  <td>B1</td>
                  <td>-6.647</td>
                  <td>0.032</td>
                </tr>
                <tr>
                  <td>B2</td>
                  <td>70.393</td>
                  <td>0.032</td>
                </tr>
                <tr>
                  <td>B12</td>
                  <td>224.764</td>
                  <td>0.032</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>то для параметра В1	наблюдаемое значение критерия Стьюдента:</p>
        <p>Набл_Ст = 6.647 / 0.18 = 37.16</p>
        <p>Для остальных параметров:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Обозначение</th>
                  <th>Набл_Ст</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>B0</td>
                  <td>4.97</td>
                </tr>
                <tr>
                  <td>B1</td>
                  <td>37.16</td>
                </tr>
                <tr>
                  <td>B2</td>
                  <td>393.51</td>
                </tr>
                <tr>
                  <td>B12</td>
                  <td>1256.47</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Число степеней свободы критерия Стьюдента - число степеней свободы дисперсии воспроизводимости, т.е. следующая величина: </p>
        <p>(m-1) * N.</p>
        <p>В результате проверки значимости устанавливается статистическая значимость или незначимость отличия от нуля оценок параметров полученной модели, т.е. выясняется, обусловлено ли отличие коэффициента от нуля чисто случайными обстоятельствами, влиянием помехи или же это отличие не случайно и вызвано тем, что в теоретической регрессионной модели присутствует соответствующий не равный нулю коэффициент регрессии.</p>
        <p>Проверка значимости оценок коэффициентов производится раздельно для оценки каждого коэффициента. При этом проверка значимости сводится к последовательной проверке гипотез вида:
          <ol start="0">
            <li>“Рассматриваемый коэффициент незначимо отличается от нуля”,</li>
            <li>“Рассматриваемый коэффициент нулю не равен”.</li>
          </ol>
        </p>
        <p>Для проверки этих гипотез используется критерий Стьюдента:<br>
если наблюдаемое значение критерия Стьюдента больше критического значения критерия Стьюдента на выбранном уровне значимости, то нулевая гипотеза должна быть отвергнута; следовательно, отличие рассматриваемой оценки от нуля не случайно, этот коэффициент статистически значим и должен быть сохранен в уравнении регрессии. 
</p>
        <p>В противном случае нулевая гипотеза принимается.</p>
        <p>Например, если наблюдаемое значение критерия Стьюдента для параметров:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Обозначение</th>
                  <th>Набл_Ст</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>B0</td>
                  <td>4.97</td>
                </tr>
                <tr>
                  <td>B1</td>
                  <td>37.16</td>
                </tr>
                <tr>
                  <td>B2</td>
                  <td>393.51</td>
                </tr>
                <tr>
                  <td>B12</td>
                  <td>1256.47</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>а критическое: Крит_Ст(8, 0.05) = 2.306,<br>то гипотезы о незначимости параметров отвергаются на уровне значимости а = 0.05, таким образом, для рассматриваемого примера все параметры значимы.</p>
        <p>С физической точки зрения может существовать несколько причин, по которым коэффициент регрессии при определенной переменной оказывается незначимым:
          <ol>
            <li>переменная действительно не влияет на отклик объекта;</li>
            <li>действие переменной не проявилось на фоне помехи, следовательно имеет смысл изменить интервал варьирования фактора или увеличить число параллельных опытов и попытаться еще раз провести эксперимент.</li>
          </ol>
        </p>
        <p>В случае, если коэффициент регрессии оказался незначимым, и предполагается, что незначимость обусловлена тем, что соответствующая базисная функция не влияет на отклик объекта, его стоит исключить из модели. Но необходимо учитывать, что, если в ортогональных планах оценки параметров некоррелированы, и исключение одного из параметров не требует пересчета всех остальных, то в планах, не обладающих свойством ортогональности, уточнение модели сопряжено с пересчетом всех остающихся параметров, т.к. получаемые оценки взаимозависимы.</p>
        <p>Число степеней свободы дисперсии адекватности число точек спектра плана N минус количество измерений, использованных для вычисления значимых коэффициентов: для N-d.</p>
        <p>Значение отклика по модели в некоторой точки ФП - численное значение, полученное в результате подстановки в уравнении регрессии значений факторов, соответствующих указанной точке плана.</p>
        <p>В работе рассматривается нормированная модель, т.е. модель, параметры которой рассчитаны для нормированных значений факторов.</p>
        <p>Например, пусть требуется вычислить значения отклика по модели двухфакторного объекта ( n = 2 ) первого порядка, имеющего следующий список существенных переменнных:</p>
        <p>1, Х1, Х2, Х1*Х2 .</p>
        <p>Дана матрица спектра плана:<br>ПФЭ, m=2, N=4</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка плана</th>
                  <th>Х1</th>
                  <th>Х2</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>+1</td>
                  <td>+1</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-1</td>
                  <td>+1</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>+1</td>
                  <td>-1</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>-1</td>
                  <td>-1</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Параметры нормированной модели имеют следующие значения:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Обозначение</th>
                  <th>Оценка</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>B0</td>
                  <td>-0.891</td>
                </tr>
                <tr>
                  <td>B1</td>
                  <td>-6.647</td>
                </tr>
                <tr>
                  <td>B2</td>
                  <td>70.393</td>
                </tr>
                <tr>
                  <td>B12</td>
                  <td>224.764</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Тогда значение отклика по модели в третьей точке плана считается так:</p>
        <p>y = - 0.891 - 6.647*1 + 70.393*(-1) + 224.764 * 1 * (-1) = -302.70</p>
        <p>Для остальных точек спектра плана:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка плана</th>
                  <th>Отклик по модели</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>287.63</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-148.62</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>-302.70</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>160.13</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Средние значения отклика, полученные экспериментальным путем, вообще говоря, могут не совпадать со значениями отклика, вычисленными по модели, следовательно разности среднего значения и предсказанного значения отклика несут информации об ошибках предсказания по уравнению регрессии.</p>
        <p>Для анализа свойств полученной модели вычисляется дисперсия адекватности, которая интегрально оценивает степень рассеяния экспериментальных данных относительно линии регрессии.</p>
        <p>Если число степеней свободы дисперсии адекватности равно нулю, то вычисление дисперсии адекватности оказывается невозможным. Возникновение такой ситуации возможно для насыщенных планов - планов, у которых число точек спектра равно количеству параметров модели, которые требуется оценить, когда все вычисляемые коэффициенты оказываются значимыми.</p>
        <p>В этом случае необходимо провести дополнительные опыты в некоторой точке факторного пространства, тем самым увеличив число точек спектра плана по сравнению с количеством значимых коэффициентов d.</p>
        <p>Проведение нескольких параллельных опытов в дополнительной точке дает 1 степень свободы для дисперсии адекватности.</p>
        <p>Например, пусть для исследования двухфакторного объекта n = 2 используется ПФЭ; рассматриваются две ситуации:
          <ol>
            <li>все параметры модели оказались значимыми;</li>
            <li>параметр ВО был признан незначимым и исключен из модели.</li>
          </ol><br>Требуется найти дисперсию адекватности для обоих случаев.
        </p>
        <p>1. Все параметры модели значимы.<br>Т.к. для ПФР N = 4 и все параметры модели двухфакторного объекта ( BO, B1, B2, B12 ) оказались значимыми - d = 4, то количество степеней свободы дисперсии адекватности N - d равно нулю. Следовательно для вычисления дисперсии адекватности придется провести дополнительный эксперимент, что добавит одну степень свободы; тогда дисперсия адекватности рассчитывается по формуле:</p>
        <p>Дисп_адекв = m(у -B0)^2</p>
        <p>Пусть в дополнительном эксперименте получены значения отклика:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th rowspan="2">Точка ФП</th>
                  <th colspan="3">Паралелльные опыты</th>
                </tr>
                <tr>
                  <th>1</th>
                  <th>2</th>
                  <th>3</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>5</td>
                  <td>-0.42</td>
                  <td>-0.42</td>
                  <td>-0.42</td>
                </tr>
              </tbody>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Найдена оценка параметра B0:</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <tr>
                <th>Обозначение</th>
                <th>Оценка</th>
              </tr>
              <tr>
                <td>В0</td>
                <td>-0.891</td>
              </tr>
            </table>
          </b-col>
          <b-col cols="9"></b-col>
        </b-row>
        <p>Для расчета потребуется найти среднее значение отклика в дополнительном эксперименте:</p>
        <p>y = (-0.42 - 0.42 - 0.42)/3 = -0.42</p>
        <p>Тогда дисперсия адекватности будет рассчитываться так:</p>
        <p>Дисп_адекв = 3*(-0,42-(-0,891))^2 = 0.66</p>
        <p>2. Параметр ВО незначим.<br>В этом случае для расчета дисперсии адекватности понадобятся следующие данные: средние значения отклика во всех точках спектра плана и значения отклика, полученные по модели, и дисперсия адекватности будет вычисляться по формуле:
        </p>
        <p>Дисп_адекв = (m / (N - d)) × Сумма,</p>
        <p>где Сумма - это сумма квадратов разностей средних значений отклика, полученных в эксперименте, и значений отклика, полученных по модели.</p>
        <p>Пусть имеются следующие данные (отклик рассчитан по приведенной здесь уточненной модели - с исключенным параметров В0)</p>
        <b-row>
          <b-col cols="3">
            <table class="table table-bordered">
              <tr>
                <th>Обозначение</th>
                <th>Оценка</th>
              </tr>
              <tr>
                <td>В1</td>
                <td>-6.647</td>
              </tr>
              <tr>
                <td>B2</td>
                <td>70.393</td>
              </tr>
              <tr>
                <td>B12</td>
                <td>224.764</td>
              </tr>
            </table>
          </b-col>
          <b-col cols="3">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th>Точка плана</th>
                  <th>Среднее значение</th>
                  <th>Отклик по модели</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td>287.62</td>
                  <td>288.62</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td>-148.62</td>
                  <td>-147.72</td>
                </tr>
                <tr>
                  <td>3</td>
                  <td>-302.70</td>
                  <td>-301.80</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td>160.13</td>
                  <td>161.02</td>
                </tr>
              </tbody>
            </table>
          </b-col>
        </b-row>
        <p>Число параллельных опытов = 3.<br>Число точек спектра плана N = 4.<br>Число значимых параметров d = 3.
        </p>
        <p>Дисп_адекв = ( 3 / (4 - 3) ) * 2<br>* ( (287.62 - 288.62)^2 + (-148.62 + 147.72)^2 +<br>+ (-302.70 + 301.80)^2 + (160.13 - 161.02)^2 ) =<br>= 9.60
        </p>
        <p>Наблюдаемое значение критерия Фишера - отношение дисперсии адекватности к дисперсии воспроизводимости.</p>
        <p>Например, пусть:<br>Дисп_адекв = 0.66,<br>Дисп_воспр = 0.39,
        </p>
        <p>тогда наблюдаемое значение критерия Фишера:<br>Набл_Фиш = 0.66 / 0.39 = 1.707
        </p>
        <p>Число степеней свободы числителя критерия Фишера - число степеней свободы, связанных с дисперсией адекватности: 
          <ol>
            <li>разность числа точек спектра плана N и количества измерений, потребовавшихся для вычисления значимых параметров модели d: N-d;</li>
            <li>в случае, если N-d = 0, то для вычисления дисперсии адекватности проводится дополнительный эксперимент, что добавляет одну степень свободы, т.о. в этом случае число степеней свободы числителя критерия Фишера - 1</li>
          </ol>
        </p>
        <p>Число степеней свободы знаменателя критерия Фишера - число степеней свободы, связанных с дисперсией воспроизводимости:</p>
        <p>N * (m-1).</p>
        <p>Проверка адекватности осуществляется путем сопоставления выборочных дисперсий адекватности и воспроизводимости. Для модели, адекватной реальному объекту, единственная причина, по которой дисперсия адекватности может отличаться от нуля, - это воздействие шума.</p>
        <p>При этом проверка адекватности сводится к проверке гипотез вида:
          <ol start="0">
            <li>“Дисперсии воспроизводимости и адекватности оценивают одну и ту же величину - дисперсию шума”,</li>
            <li>“Дисперсия адекватности систематически превышает дисперсию воспроизводимости”</li>
          </ol>
        </p>
        <p>Проверку адекватности проводят с помощью критерия Фишера:<br>если наблюдаемое значение критерия Фишера меньше критического значения критерия Фишера, то принимается нулевая гипотеза об однородности дисперсий адекватности и воспроизводимости и модель считается адекватной на выбранном уровне значимости.
        </p>
        <p>В противном случае модель считается неадекватной отклику объекта, вследствие наличия дополнительного рассеяния, обусловленного несоответствием модели и реального объекта.</p>
        <p>Например, если наблюдаемое значение критерия Фишера:<br>Набл_Фиш = 1.707,<br>а критическое: Крит_Фиш(1, 8, 0.05) = 5.035,<br>то гипотеза об адекватности модели принимается на уровне значимости а = 0.05.</p>
      </b-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  created() {},
  data() {
    return {
      significance: 0.01,
      significance_answer: "",
      params_index: [],
      params_list: ["B0", "B1", "B2", "B12"],
      params: ["B0", "B1", "B2", "B12"],
      param_1: 0,
      param_2: 0,
      param_answer: "",
      vals: [],
      df: [],
      check_df: 0,
      df_answer: "",
      crit_value: 0,
      prac_values: [],
      param_values: [],
      sign_values: [],
      sign_answer: "",
      sign_wrong: "",
      endpoints: [
        "http://127.0.0.1:5000/api/set/significance_level_student",
        "http://127.0.0.1:5000/api/get/params_for_check", 
        "http://127.0.0.1:5000/api/check/params_for_check", 
        "http://127.0.0.1:5000/api/get/student_table", 
        "http://127.0.0.1:5000/api/check/df_student", 
        "http://127.0.0.1:5000/api/check/sign_param", 
        "http://127.0.0.1:5000/api/get/sign_params"]
    };
  },
  props: {},
  methods: {
    send_significance: function (e) {
      axios
        .post(this.endpoints[0], { data: { significance: this.significance } })
        .then((response) => {
          if (!response.data.error) {
            document.getElementById("send_sign").disabled = true;
            document.getElementById("significance").style.display = "none";
            document.getElementById("param_1").style.display = "block";
            axios
            .get(this.endpoints[1])
            .then((response) => {
              if (!response.data.error) {
                let params = ["B0", "B1", "B2", "B12"];
                this.params = [params[response.data.data.params[0]], params[response.data.data.params[1]]]
                this.params_index = [response.data.data.params[0], response.data.data.params[1]]
              } else {
                this.significance_answer = response.data.message
              }
            })
            .catch((error) => {
              console.log("-----error-------");
              console.log(error);
            });
          } else {
            this.significance_answer = response.data.message
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    display_param_2: function (e) {
            document.getElementById("param_1").style.display = "none";
            document.getElementById("param_2").style.display = "block";
    },
    send_params: function (e) {
      axios
        .post(this.endpoints[2], { data: { 
          first_param: this.param_1, 
          second_param: this.param_2, } })
        .then((response) => {
          if (!response.data.error) {
            document.getElementById("param_1_btn").disabled = true;
            document.getElementById("param_1").style.display = "none";
            document.getElementById("param_2").style.display = "none";
            axios
            .get(this.endpoints[3])
            .then((response) => {
              if (!response.data.error) {
                this.vals = response.data.data.vals;
                this.df = response.data.data.df;
              } else {
                this.param_answer = response.data.message
              }
            })
            .catch((error) => {
              console.log("-----error-------");
              console.log(error);
            });
            document.getElementById("crit_values").style.display = "block";
          } else {
            this.param_answer = response.data.message
            if (response.data.message.indexOf("first_param") != -1){
              document.getElementById("param_1").style.display = "block";
              document.getElementById("param_1_btn").style.display = "none";

            }
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    send_check_df: function (e) {
      axios
        .post(this.endpoints[4], { data: { 
          df_student: this.check_df,  } })
        .then((response) => {
          if (!response.data.error) {
            this.crit_value = response.data.data.crit_val;
            this.prac_values = response.data.data.prac;
            document.getElementById("crit_values").style.display = "none";
            document.getElementById("sign_1").style.display = "block";
          } else {
            this.df_answer = response.data.message
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
    is_sign: function(answer, index) {
      axios
        .get(this.endpoints[6])
        .then((response) => {
          if (!response.data.error) {
            this.param_values = response.data.data.params;
            this.sign_values = response.data.data.is_sign;
            if (answer == this.sign_values[index]){
              this.sign_answer = "Правильно. Оценка параметра значима."
              if (document.getElementById("sign_1").style.display == "block"){
                document.getElementById("sign_1").style.display = "none";
                document.getElementById("sign_2").style.display = "block";
              }
              else if (document.getElementById("sign_2").style.display == "block"){
                document.getElementById("sign_2").style.display = "none";
                document.getElementById("sign_table").style.display = "block";
              }
            }
            else {
              this.sign_answer = "Неправильно."
            }
          } else {
            this.sign_wrong = response.data.message
          }
        })
        .catch((error) => {
          console.log("-----error-------");
          console.log(error);
        });
    },
  },
};
</script>

<style scoped></style>

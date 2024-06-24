/**
 * Здесь нужно перегружать объекты и дополнять функционал.
 * Этот файл подключается последним.
 */

/**
 * Реализация bind, если таковой нет (для поддержки в IE)
 */
if (!Function.prototype.bind) {
  Function.prototype.bind = function(oThis) {
    if (typeof this !== 'function') {
      // closest thing possible to the ECMAScript 5
      // internal IsCallable function
      throw new TypeError('Function.prototype.bind - what is trying to be bound is not callable');
    }

    var aArgs   = Array.prototype.slice.call(arguments, 1),
        fToBind = this,
        fNOP    = function() {},
        fBound  = function() {
          return fToBind.apply(this instanceof fNOP && oThis
                 ? this
                 : oThis,
                 aArgs.concat(Array.prototype.slice.call(arguments)));
        };

    fNOP.prototype = this.prototype;
    fBound.prototype = new fNOP();

    return fBound;
  };
}

/**
 * Необходимо для фикса ошибки "parentNode null or not an object" в IE10
 */
Ext.override(Ext.Element, {

    /**
    * Inserts this element after the passed element in the DOM
    * @param {Mixed} el The element to insert after
    * @return {Ext.Element} this
    *
    * @overrides  to fix IE issue of "parentNode null or not an object".
    */
    insertAfter: function(el){
        el = Ext.getDom(el);
        if (el && el.parentNode) {
            el.parentNode.insertBefore(this.dom, el.nextSibling);
        }
        return this;
    }
});


/**
 * Нужно для правильной работы окна
 */
Ext.onReady(function () {
    Ext.override(Ext.Window, {

        /*
         *  Если установлена модальность и есть родительское окно, то
         *  флаг модальности помещается во временную переменную tmpModal, и
         *  this.modal = false;
         */
        tmpModal: false,
        manager: new Ext.WindowGroup(),
        // 2011.01.14 kirov
        // убрал, т.к. совместно с desktop.js это представляет собой гремучую смесь
        // кому нужно - пусть прописывает Ext.getBody() в своем "десктопе" на onReady или когда хочет
        //,renderTo: Ext.getBody().id
        constrain: true,
        /**
         * Выводит окно на передний план
         * Вызывается в контексте дочернего
         * по отношению к parentWindow окну
         */
        activateChildWindow: function () {
            this.toFront();
        },
        listeners: {

            'beforeshow': function () {
                var renderTo = Ext.get(this.renderTo);
                if (renderTo) {
                    if (renderTo.getHeight() < this.getHeight())
                        this.setHeight(renderTo.getHeight());
                }

                if (this.parentWindow) {

                    this.parentWindow.setDisabled(true);

                    /*
                     * В Extjs 3.3 Добавили общую проверку в функцию mask, см:
                     *  if (!(/^body/i.test(dom.tagName) && me.getStyle('position') == 'static')) {
                     me.addClass(XMASKEDRELATIVE);
                     }
                     *
                     * было до версии 3.3:
                     *  if(!/^body/i.test(dom.tagName) && me.getStyle('position') == 'static'){
                     me.addClass(XMASKEDRELATIVE);
                     }
                     * Теперь же расположение замаскированых окон должно быть относительным
                     * (relative) друг друга
                     *
                     * Такое поведение нам не подходит и другого решения найдено не было.
                     * Кроме как удалять данный класс
                     * */
                    this.parentWindow.el.removeClass('x-masked-relative');

                    this.parentWindow.on('activate', this.activateChildWindow, this);

                    this.modal = false;
                    this.tmpModal = true;

                    if (window.AppDesktop) {
                        var el = AppDesktop.getDesktop().taskbar.tbPanel.getTabWin(this.parentWindow);
                        if (el) {
                            el.mask();
                        }
                    }
                }
                if (this.modal) {
                    var taskbar = Ext.get('ux-taskbar');
                    if (taskbar) {
                        taskbar.mask();
                    }
                    var toptoolbar = Ext.get('ux-toptoolbar');
                    if (toptoolbar) {
                        toptoolbar.mask();
                    }
                }
            },
            close: function () {
                if (this.tmpModal && this.parentWindow) {
                    this.parentWindow.un('activate', this.activateChildWindow, this);
                    this.parentWindow.setDisabled(false);
                    this.parentWindow.toFront();

                    if (window.AppDesktop) {
                        var el = AppDesktop.getDesktop().taskbar.tbPanel.getTabWin(this.parentWindow);
                        if (el) {
                            el.unmask();
                        }
                    }
                }

                if (this.modal) {
                    var taskbar = Ext.get('ux-taskbar');
                    if (taskbar) {
                        taskbar.unmask();
                    }
                    var toptoolbar = Ext.get('ux-toptoolbar');
                    if (toptoolbar) {
                        toptoolbar.unmask();
                    }
                }
            },
            hide: function () {
                if (this.modal) {
                    if (!this.parentWindow) {
                        var taskbar = Ext.get('ux-taskbar');
                        if (taskbar) {
                            taskbar.unmask();
                        }
                        var toptoolbar = Ext.get('ux-toptoolbar');
                        if (toptoolbar) {
                            toptoolbar.unmask();
                        }
                    }
                }
            }
        }
    });
});

/**
 * Обновим TreeGrid чтобы колонки занимали всю ширину дерева
 */
Ext.override(Ext.ux.tree.TreeGrid, {

    // добавлено
    fitColumns: function () {
        var nNewTotalWidth = this.getInnerWidth() - Ext.num(this.scrollOffset, Ext.getScrollBarWidth());
        var nOldTotalWidth = this.getTotalColumnWidth();
        var cs = this.getVisibleColumns();
        var n, nUsed = 0;

        for (n = 0; n < cs.length; n++) {
            if (n == cs.length - 1) {
                cs[n].width = nNewTotalWidth - nUsed - 1;
                break;
            }
            cs[n].width = Math.floor((nNewTotalWidth / 100) * (cs[n].width * 100 / nOldTotalWidth)) - 1;
            nUsed += cs[n].width;
        }

        this.updateColumnWidths();
    },
    // <--
    onResize: function (w, h) {
        Ext.ux.tree.TreeGrid.superclass.onResize.apply(this, arguments);

        var bd = this.innerBody.dom;
        var hd = this.innerHd.dom;

        if (!bd) {
            return;
        }

        if (Ext.isNumber(h)) {
            bd.style.height = this.body.getHeight(true) - hd.offsetHeight + 'px';
        }

        if (Ext.isNumber(w)) {
            var sw = Ext.num(this.scrollOffset, Ext.getScrollBarWidth());
            if (this.reserveScrollOffset || ((bd.offsetWidth - bd.clientWidth) > 10)) {
                this.setScrollOffset(sw);
            } else {
                var me = this;
                setTimeout(function () {
                    me.setScrollOffset(bd.offsetWidth - bd.clientWidth > 10 ? sw : 0);
                }, 10);
            }
        }
        this.fitColumns(); // добавилась/заменила
    }
});

Ext.override(Ext.tree.ColumnResizer, {
    onEnd: function () {
        var nw = this.proxy.getWidth(),
            tree = this.tree;

        this.proxy.remove();
        delete this.dragHd;

        tree.columns[this.hdIndex].width = nw;
        //tree.updateColumnWidths(); // закомментировано
        tree.fitColumns();			// добавлено

        setTimeout(function () {
            tree.headersDisabled = false;
        }, 100);
    }
});

/**
 * Обновим ячейку дерева чтобы при двойном клике не открывались/сворачивались дочерние узлы
 */
Ext.override(Ext.tree.TreeNodeUI, {
    onDblClick: function (e) {
        e.preventDefault();
        if (this.disabled) {
            return;
        }
        if (this.fireEvent("beforedblclick", this.node, e) !== false) {
            if (this.checkbox) {
                this.toggleCheck();
            }
            // закомментировано.
            //if(!this.animating && this.node.isExpandable()){
            //    this.node.toggle();
            //}
            this.fireEvent("dblclick", this.node, e);
        }
    }
});
/**
 * Исправим ошибку, когда значения emptyText в композитном поле передаются на сервер,
 * даже если установлен признак "не передавать"
 */
Ext.override(Ext.form.Action.Submit, {
    run : function(){
        var o = this.options,
            method = this.getMethod(),
            isGet = method == 'GET';
        if(o.clientValidation === false || this.form.isValid()){
            if (o.submitEmptyText === false) {
                var fields = this.form.items,
                    emptyFields = [],
                    setupEmptyFields = function(f){
                        // M prefer: field (например, combobox) может быть неотрендеренный
                        if (f.rendered && f.el.getValue() == f.emptyText) {
                        // if (f.el.getValue() == f.emptyText) {
                            emptyFields.push(f);
                            f.el.dom.value = "";
                        }
                        // M prefer: rendered проверяется выше
                        if(f.isComposite){
                        // if(f.isComposite && f.rendered){
                            f.items.each(setupEmptyFields);
                        }
                    };

                fields.each(setupEmptyFields);
            }
            Ext.Ajax.request(Ext.apply(this.createCallback(o), {
                form:this.form.el.dom,
                url:this.getUrl(isGet),
                method: method,
                headers: o.headers,
                params:!isGet ? this.getParams() : null,
                isUpload: this.form.fileUpload
            }));
            if (o.submitEmptyText === false) {
                Ext.each(emptyFields, function(f) {
                    if (f.applyEmptyText) {
                        f.applyEmptyText();
                    }
                });
            }
        }else if (o.clientValidation !== false){ // client validation failed
            this.failureType = Ext.form.Action.CLIENT_INVALID;
            this.form.afterAction(this, false);
        }
    }
});

/**
 * Метод  вызывается и при клике и при событии change - сюда добавлена обработка
 * атрибута readOnly, тк в стандартном поведении браузеры обрабаытвают этот атрибут только
 * у текстоввых полей
 */
Ext.override(Ext.form.Checkbox, {
    onClick: function (e) {
        if (this.readOnly) {
            e.stopEvent();
            return false;
        }

        if (this.el.dom.checked != this.checked) {
            this.setValue(this.el.dom.checked);
        }
    }
});

/**
 * Раньше нельзя было перейти на конкретную страницу в движках webkit. Т.к.
 * Событие PagingBlur наступает раньше pagingChange, и обновлялась текущая
 * страница, т.к. PagingBlur обновляет индекс.
 */
Ext.override(Ext.PagingToolbar, {
    onPagingBlur: Ext.emptyFn
});

/*
 * Проблема скроллинга хидеров в компонентах ExtPanel или ExtFieldSet
 * (Скролятся только хидеры)
 */

if (Ext.isIE7 || Ext.isIE6) {
    Ext.Panel.override({
        setAutoScroll: function () {
            if (this.rendered && this.autoScroll) {
                var el = this.body || this.el;
                if (el) {
                    el.setOverflow('auto');
                    // Following line required to fix autoScroll
                    el.dom.style.position = 'relative';
                }
            }
        }
    });
}

/**
 * добавим поддержку чекбоксов по аналогии с TreePanel
 * чек боксы включаются просто передачей checked в сторе
 */
Ext.override(Ext.ux.tree.TreeGridNodeUI, {
    renderElements: function (n, a, targetNode, bulkRender) {
        var t = n.getOwnerTree(),
            cb = Ext.isBoolean(a.checked),
            cols = t.columns,
            c = cols[0],
            i, buf, len;

        this.indentMarkup = n.parentNode ? n.parentNode.ui.getChildIndent() : '';

        buf = [
            '<tbody class="x-tree-node">',
            '<tr ext:tree-node-id="', n.id , '" class="x-tree-node-el x-tree-node-leaf x-unselectable ', a.cls, '">',
            '<td class="x-treegrid-col">',
            '<span class="x-tree-node-indent">', this.indentMarkup, "</span>",
            '<img src="', this.emptyIcon, '" class="x-tree-ec-icon x-tree-elbow" />',
            '<img src="', a.icon || this.emptyIcon, '" class="x-tree-node-icon', (a.icon ? " x-tree-node-inline-icon" : ""), (a.iconCls ? " " + a.iconCls : ""), '" unselectable="on" />',
            cb ? ('<input class="x-tree-node-cb" type="checkbox" ' + (a.checked ? 'checked="checked" />' : '/>')) : '',
            '<a hidefocus="on" class="x-tree-node-anchor" href="', a.href ? a.href : '#', '" tabIndex="1" ',
            a.hrefTarget ? ' target="' + a.hrefTarget + '"' : '', '>',
            '<span unselectable="on">', (c.tpl ? c.tpl.apply(a) : a[c.dataIndex] || c.text), '</span></a>',
            '</td>'
        ];

        for (i = 1, len = cols.length; i < len; i++) {
            c = cols[i];
            buf.push(
                '<td class="x-treegrid-col ', (c.cls ? c.cls : ''), '">',
                '<div unselectable="on" class="x-treegrid-text"', (c.align ? ' style="text-align: ' + c.align + ';"' : ''), '>',
                (c.tpl ? c.tpl.apply(a) : a[c.dataIndex]),
                '</div>',
                '</td>'
            );
        }

        buf.push(
            '</tr><tr class="x-tree-node-ct"><td colspan="', cols.length, '">',
            '<table class="x-treegrid-node-ct-table" cellpadding="0" cellspacing="0" style="table-layout: fixed; display: none; width: ', t.innerCt.getWidth(), 'px;"><colgroup>'
        );
        for (i = 0, len = cols.length; i < len; i++) {
            buf.push('<col style="width: ', (cols[i].hidden ? 0 : cols[i].width), 'px;" />');
        }
        buf.push('</colgroup></table></td></tr></tbody>');

        if (bulkRender !== true && n.nextSibling && n.nextSibling.ui.getEl()) {
            this.wrap = Ext.DomHelper.insertHtml("beforeBegin", n.nextSibling.ui.getEl(), buf.join(''));
        } else {
            this.wrap = Ext.DomHelper.insertHtml("beforeEnd", targetNode, buf.join(''));
        }

        this.elNode = this.wrap.childNodes[0];
        this.ctNode = this.wrap.childNodes[1].firstChild.firstChild;
        var cs = this.elNode.firstChild.childNodes;
        this.indentNode = cs[0];
        this.ecNode = cs[1];
        this.iconNode = cs[2];
        var index = 3;
        if (cb) {
            this.checkbox = cs[3];
            // fix for IE6
            this.checkbox.defaultChecked = this.checkbox.checked;
            index++;
        }
        this.anchor = cs[index];
        this.textNode = cs[index].firstChild;
    }
});

/**
 * добавим поддержку чекбоксов по аналогии с TreePanel
 * чек боксы включаются просто передачей checked в сторе
 */
Ext.override(Ext.ux.tree.TreeGrid, {

    /**
     * Retrieve an array of checked nodes, or an array of a specific attribute of checked nodes (e.g. 'id')
     * @param {String} a (optional) Defaults to null (return the actual nodes)
     * @param {TreeNode} startNode (optional) The node to start from, defaults to the root
     * @return {Array}
     */
    getChecked: function (a, startNode) {
        startNode = startNode || this.root;
        var r = [];
        var f = function () {
            if (this.attributes.checked) {
                r.push(!a ? this : (a == 'id' ? this.id : this.attributes[a]));
            }
        };
        startNode.cascade(f);
        return r;
    }
});

/**
 * По-умолчанию ExtJS отправляет за картинкой на 'http://www.extjs.com/s.gif'
 * Тут укажем что они не правы
 */
Ext.apply(Ext, function () {
    return {
        BLANK_IMAGE_URL: Ext.isIE6 || Ext.isIE7 || Ext.isAir ?
            '/m3static/vendor/extjs/resources/images/default/s.gif' :
            'data:image/gif;base64,R0lGODlhAQABAID/AMDAwAAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
    };
}());


/**
 * Исправление поведения Ext.ComboBox, когда значения списка с value '' и 0
 * считаются идентичными: теперь сравнение происходит с приведением к строке.
 * Описание ошибки и патч отсюда: http://www.sencha.com/forum/showthread.php?79285
 */
Ext.override(Ext.form.ComboBox, {
    findRecord: function (prop, value) {
        var record;
        if (this.store.getCount() > 0) {
            this.store.each(function (r) {
                if (String(r.data[prop]) == String(value)) {
                    record = r;
                    return false;
                }
            });
        }
        return record;
    }
});

/**
 * Добавление/удаление пользовательского класса m3-grey-field после использования
 * setReadOnly для Ext.form.Field и Ext.form.TriggerField
 * см m3.css - стр. 137 .m3-grey-field
 */
var setReadOnlyField = Ext.form.Field.prototype.setReadOnly.bind({});
var restoreClass = function (readOnly) {
    if (readOnly) {
        this.addClass('m3-grey-field');
        this.el.dom.setAttribute('readonly', '');
    } else {
        this.removeClass('m3-grey-field');
        this.el.dom.removeAttribute('readonly');
    }
};

Ext.override(Ext.form.Field, {
    setReadOnly: function (readOnly) {
        if(readOnly || !(this.ownerCt && this.ownerCt.readOnly)){
            setReadOnlyField.call(this, readOnly);
            restoreClass.call(this, readOnly);
        }
    }
});

var setReadOnlyTriggerField = Ext.form.TriggerField.prototype.setReadOnly;
Ext.override(Ext.form.TriggerField, {
    setReadOnly: function (readOnly) {
        if(readOnly || !(this.ownerCt && this.ownerCt.readOnly)){
            setReadOnlyTriggerField.call(this, readOnly);
            restoreClass.call(this, readOnly);
        }
    }
});

/**
 * #77796 Фикс для корректировки последней колонки в гриде
 * Было:
 *     colModel.setColumnWidth(i, Math.max(grid.minColumnWidth, Math.floor(colWidth + colWidth * fraction)), true);
 * стало:
 *     colModel.setColumnWidth(i, Math.floor(colWidth + colWidth * fraction), true);
 */
Ext.override(Ext.grid.GridView, {
    fitColumns: function (preventRefresh, onlyExpand, omitColumn) {
        var grid = this.grid,
            colModel = this.cm,
            totalColWidth = colModel.getTotalWidth(false),
            gridWidth = this.getGridInnerWidth(),
            extraWidth = gridWidth - totalColWidth,
            columns = [],
            extraCol = 0,
            width = 0,
            colWidth, fraction, i;


        if (gridWidth < 20 || extraWidth === 0) {
            return false;
        }

        var visibleColCount = colModel.getColumnCount(true),
            totalColCount = colModel.getColumnCount(false),
            adjCount = visibleColCount - (Ext.isNumber(omitColumn) ? 1 : 0);

        if (adjCount === 0) {
            adjCount = 1;
            omitColumn = undefined;
        }


        for (i = 0; i < totalColCount; i++) {
            if (!colModel.isFixed(i) && i !== omitColumn) {
                colWidth = colModel.getColumnWidth(i);
                columns.push(i, colWidth);

                if (!colModel.isHidden(i)) {
                    extraCol = i;
                    width += colWidth;
                }
            }
        }

        fraction = (gridWidth - colModel.getTotalWidth()) / width;

        while (columns.length) {
            colWidth = columns.pop();
            i = columns.pop();

            colModel.setColumnWidth(i, Math.floor(colWidth + colWidth * fraction), true);
        }


        totalColWidth = colModel.getTotalWidth(false);

        if (totalColWidth > gridWidth) {
            var adjustCol = (adjCount == visibleColCount) ? extraCol : omitColumn,
                newWidth = Math.max(1, colModel.getColumnWidth(adjustCol) - (totalColWidth - gridWidth));

            colModel.setColumnWidth(adjustCol, newWidth, true);
        }

        if (preventRefresh !== true) {
            this.updateAllColumnWidths();
        }

        return true;
    }
});

/**
* В ExtJS по какой-то причине используется parseInt что приводит к ошибкам
* при обработке дробных значений
* было size = side && parseInt(this.getStyle(styles[side]), 10)
* стало size = side && parseFloat(this.getStyle(styles[side]))
*/
Ext.override(Ext.Element, {
    addStyles : function(sides, styles){
        var ttlSize = 0,
            sidesArr = sides.match(/\w/g),
            side,
            size,
            i,
            len = sidesArr.length;
        for (i = 0; i < len; i++) {
            side = sidesArr[i];
            size = side && parseFloat(this.getStyle(styles[side]));
            if (size) {
                ttlSize += Math.abs(size);
            }
        }
        return ttlSize;
    }
});

/**
 * BOBUH-19922 Добавлен вызов ивента beforeaddmenuitem перед добавлением элементов в контекстное меню колонки
 * Было:
 *     menu.add(new Ext.menu.CheckItem({
 *                         itemId: "col-" + cm.getColumnId(col),
 *                         text: text.join(' '),
 *                         checked: !cm.isHidden(col),
 *                         hideOnClick: false,
 *                         disabled: cm.config[col].hideable === false
 *                     }));
 * Стало:
 *     var newMenuItem = new Ext.menu.CheckItem({
 *                         itemId: "col-" + cm.getColumnId(col),
 *                         text: text.join(' '),
 *                         checked: !cm.isHidden(col),
 *                         hideOnClick: false,
 *                         disabled: cm.config[col].hideable === false
 *                     });
 *                     cm.fireEvent('beforeaddmenuitem', cm, newMenuItem);
 *                     menu.add(newMenuItem);
 */
function beforeColMenuShow(){
    var cm = this.cm,
        rows = this.cm.rows,
        menu,
        text,
        group,
        gcol,
        r,
        title;
    this.colMenu.removeAll();

    for(var col = 0, clen = cm.getColumnCount(); col < clen; col++){
        menu = this.colMenu;
        title = cm.getColumnHeader(col);
        text = [];

        if(cm.config[col].fixed !== true && cm.config[col].hideable !== false){

            for(var row = 0, rlen = rows.length; row < rlen; row++){
                r = rows[row];
                gcol = 0;

                for(var i = 0, len = r.length; i < len; i++){
                    group = r[i];

                    if(col >= gcol && col < gcol + group.colspan){
                        break;
                    }
                    gcol += group.colspan;
                }

                if(group && group.header){

                    if(cm.hierarchicalColMenu){
                        var gid = 'group-' + row + '-' + gcol,
                            item = menu.items ? menu.getComponent(gid) : null,
                            submenu = item ? item.menu : null;

                        if(!submenu){
                            submenu = new Ext.menu.Menu({
                                itemId: gid
                            });
                            submenu.on("itemclick", this.handleHdMenuClick, this);
                            var checked = false,
                                disabled = true;

                            for(var c = gcol, lc = gcol + group.colspan; c < lc; c++){

                                if(!cm.isHidden(c)){
                                    checked = true;
                                }

                                if(cm.config[c].hideable !== false){
                                    disabled = false;
                                }
                            }
                            menu.add({
                                itemId: gid,
                                text: group.header,
                                menu: submenu,
                                hideOnClick: false,
                                checked: checked,
                                disabled: disabled
                            });
                        }
                        menu = submenu;
                    }

                    else{
                        text.push(group.header);
                    }
                }
            }
            text.push(title);
            var newMenuItem = new Ext.menu.CheckItem({
                itemId: "col-" + cm.getColumnId(col),
                text: text.join(' '),
                checked: !cm.isHidden(col),
                hideOnClick: false,
                disabled: cm.config[col].hideable === false
            });
            cm.fireEvent('beforeaddmenuitem', cm, newMenuItem);
            menu.add(newMenuItem);
        }
    }
};

Ext.override(Ext.ux.grid.ColumnHeaderGroup, {
    init: function(grid){
        this.viewConfig.beforeColMenuShow = beforeColMenuShow;
        Ext.applyIf(grid.colModel, this.config);
        Ext.apply(grid.getView(),this.viewConfig);
    }
});


/**
 * Очень пытливые умы успевают за короткое время несколько раз кликнуть на кнопку. Не спасает даже disabled, потому что
 * он не успеват сработать. Это в определенных случаях приводит к неприятным последствиям. Например, один документ
 * может сохраниться дважды и в этом случае мы получаем копии, которые нам не нужны.
 * Поэтому делаем финт ушами и запоминаем момент последнего клика на кнопке и в течение ближайших 500 миллисекунд не
 * дадим повторно выполнить это же действие.
 */
Ext.override(Ext.Button, {
    onClick: function(e) {
        var me = this,
            now = Date.now();

        if (now < me.lastClickTimestamp + 500) {
            me.lastClickTimestamp = now;
            return;
        }
        me.lastClickTimestamp = now;

        if (e) {
            e.preventDefault();
        }
        if (e.button !== 0) {
            return;
        }
        if (!this.disabled) {
            this.doToggle();
            if (this.menu && !this.hasVisibleMenu() && !this.ignoreNextClick) {
                this.showMenu();
            }
            this.fireEvent('click', this, e);
            if (this.handler) {

                this.handler.call(this.scope || this, this, e);
            }
        }
    }
});


Ext.override(Ext.m3.AdvancedDataField, {
    onBlur : function(){
	/*
	   В суперклассе Ext.form.TriggerField данный метод перекрывается пустой функцией,
   	   видимо для того, чтобы все изменения и событие change происходили только при нажатии на триггеры,
 	   но данное поведение весьма неудобно в колоночных фильтрах, где требуется корректное срабатывание
       blur и change при потере фокуса. Также есть проверка для прерывания дальнейших неправильных вызовов.
	   Данная реализация метода взята из базового класса Ext.formField
	*/
        if (this.value == this.getRawValue()) {
            return;
        }

	    this.beforeBlur();
	    if(this.focusClass){
	        this.el.removeClass(this.focusClass);
	    }
	    this.hasFocus = false;
	    if(this.validationEvent !== false && (this.validateOnBlur || this.validationEvent == 'blur')){
	        this.validate();
	    }
	    var v = this.getValue();
	    if(String(v) !== String(this.startValue)){
	        this.fireEvent('change', this, v, this.startValue);
	    }
	    this.fireEvent('blur', this);
	    this.postBlur();
    }

});

function default_plot(x, y1, y2, y3, title_str, x_label_str, y_label_str)

    %% figure 양식 설정
    h=figure('Units', 'centimeters', 'Position', [5, 5, 15, 10]);
    ax = gca; %let user change axis setting
    ax.FontSize = 11; %axis fontsize 
    ax.LineWidth = 1.0; ax.FontWeight="bold"; %axis linewidth and Fontweight
    % ax.GridLineStyle = '--';
    % ax.GridLineWidth = 1;
    ax.GridColor='#202020';
    fontname(gcf,"Arial") 
    ax.Color=[0.95 0.95 0.95];
    box
    pbaspect([2.1 1 1])

    %% python에서 온 데이터 파싱
    num_data = length(y_cell);
    colors = lines(num_data);

    %% 그래프 그리기
    hold on;

    plot(x, y1, 'LineWidth', 1.5, 'LineStyle', '-', 'Color', colors(1, :));
    plot(x, y2, 'LineWidth', 1.5, 'LineStyle', '-', 'Color', colors(2, :));
    plot(x, y3, 'LineWidth', 1.5, 'LineStyle', '-', 'Color', colors(3, :));

    title(title_str,"FontSize", 12, "FontWeight", "bold");
    xlabel(x_label_str);
    ylabel(y_label_str);

    legend('acc_x', 'acc_y', 'acc_z', Location='northeast',NumColumns=3);

    grid on;
    box on;
    grid minor;
    hold off;

    saveas(h, '../figs/default_plot.png');
    drawnow;
end